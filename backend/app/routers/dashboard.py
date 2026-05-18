from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional
from app.database import get_db
from app.models.sensor import Sensor
from app.models.alert import Alert
from app.models.device import Device
from app.models.reading import Reading

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)):
    """Resumen de KPIs para la pantalla principal del dashboard."""
    active_sensors  = (await db.execute(select(func.count(Sensor.id)).where(Sensor.is_active == True))).scalar() or 0
    active_alerts   = (await db.execute(select(func.count(Alert.id)).where(Alert.status == "active"))).scalar() or 0
    devices_online  = (await db.execute(select(func.count(Device.id)).where(Device.status == "online"))).scalar() or 0
    devices_total   = (await db.execute(select(func.count(Device.id)))).scalar() or 0

    # Promedio de lecturas MQ135 de la última hora como proxy de calidad del aire
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    avg_mq135_q = (
        select(func.avg(Reading.value))
        .join(Sensor, Reading.sensor_id == Sensor.id)
        .where(Sensor.sensor_type == "MQ135", Reading.timestamp >= one_hour_ago)
    )
    avg_mq135 = (await db.execute(avg_mq135_q)).scalar() or 0.0

    # Calidad del aire: 100% = 0 ppm, 0% = 1000 ppm
    air_quality = max(0, round(100 - (avg_mq135 / 10), 1))

    return {
        "active_sensors":  active_sensors,
        "active_alerts":   active_alerts,
        "devices_online":  devices_online,
        "devices_total":   devices_total,
        "air_quality_pct": air_quality,
        "system_status":   "stable" if active_alerts == 0 else "alert",
    }

@router.get("/chart-data")
async def get_chart_data(
    sensor_type: str = Query("MQ135", description="Tipo de sensor a graficar"),
    hours: int = Query(6, ge=1, le=48, description="Horas de histórico a retornar"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retorna lecturas promediadas por hora para los gráficos del dashboard.
    Compatible con el componente Recharts del frontend.
    """
    since = datetime.utcnow() - timedelta(hours=hours)

    result = await db.execute(
        select(
            func.strftime("%Y-%m-%dT%H:00", Reading.timestamp).label("hour"),
            func.avg(Reading.value).label("avg_value"),
            func.min(Reading.value).label("min_value"),
            func.max(Reading.value).label("max_value"),
        )
        .join(Sensor, Reading.sensor_id == Sensor.id)
        .where(Sensor.sensor_type == sensor_type, Reading.timestamp >= since)
        .group_by(func.strftime("%Y-%m-%dT%H:00", Reading.timestamp))
        .order_by("hour")
    )

    rows = result.all()
    return {
        "sensor_type": sensor_type,
        "hours": hours,
        "data": [
            {
                "time":  row.hour,
                "value": round(row.avg_value, 1) if row.avg_value else 0,
                "min":   round(row.min_value, 1) if row.min_value else 0,
                "max":   round(row.max_value, 1) if row.max_value else 0,
            }
            for row in rows
        ],
    }