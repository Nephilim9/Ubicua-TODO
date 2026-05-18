from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.sensor import Sensor
from app.models.alert import Alert
from app.models.device import Device

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)):
    """
    Obtiene el resumen de KPIs para la pantalla principal.
    """
    # Conteo de sensores activos
    sensors_count = await db.execute(select(func.count(Sensor.id)).where(Sensor.is_active == True))
    
    # Conteo de alertas activas
    alerts_count = await db.execute(select(func.count(Alert.id)).where(Alert.status == 'active'))
    
    # Conteo de dispositivos online
    devices_online = await db.execute(select(func.count(Device.id)).where(Device.status == 'online'))
    
    return {
        "active_sensors": sensors_count.scalar() or 0,
        "active_alerts": alerts_count.scalar() or 0,
        "devices_online": devices_online.scalar() or 0,
        "system_status": "stable"
    }