from datetime import datetime
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from app.database import get_db
from app.models.sensor import Sensor
from app.models.reading import Reading
from app.schemas.sensor import SensorCreate, SensorResponse, SensorUpdate
from app.schemas.reading import ReadingCreate, ReadingResponse
from app.dependencies import verify_esp32_api_key
from app.exceptions import SensorNotFoundError

router = APIRouter(prefix="/sensors", tags=["Sensors"])

# --- CRUD Sensores ---
@router.get("/", response_model=List[SensorResponse])
async def list_sensors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sensor))
    return result.scalars().all()

@router.post("/", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
async def create_sensor(sensor_in: SensorCreate, db: AsyncSession = Depends(get_db)):
    new_sensor = Sensor(**sensor_in.model_dump())
    db.add(new_sensor)
    await db.commit()
    await db.refresh(new_sensor)
    return new_sensor

@router.get("/{sensor_id}", response_model=SensorResponse)
async def get_sensor(sensor_id: int, db: AsyncSession = Depends(get_db)):
    sensor = await db.get(Sensor, sensor_id)
    if not sensor:
        raise SensorNotFoundError(sensor_id)
    return sensor

@router.put("/{sensor_id}", response_model=SensorResponse)
async def update_sensor(sensor_id: int, sensor_in: SensorUpdate, db: AsyncSession = Depends(get_db)):
    sensor = await db.get(Sensor, sensor_id)
    if not sensor:
        raise SensorNotFoundError(sensor_id)
    for key, value in sensor_in.model_dump(exclude_unset=True).items():
        setattr(sensor, key, value)
    await db.commit()
    await db.refresh(sensor)
    return sensor

# --- Lecturas ---
@router.post("/readings", response_model=ReadingResponse, dependencies=[Depends(verify_esp32_api_key)])
async def post_reading(reading_in: ReadingCreate, db: AsyncSession = Depends(get_db)):
    """Ingesta de lectura desde el gateway ESP32 (requiere API Key)."""
    new_reading = Reading(**reading_in.model_dump())
    db.add(new_reading)
    await db.commit()
    await db.refresh(new_reading)
    return new_reading

@router.get("/readings/latest", response_model=List[ReadingResponse])
async def get_latest_readings(db: AsyncSession = Depends(get_db)):
    """Última lectura de cada sensor activo — usado por los KPIs del dashboard."""
    # Subquery: max timestamp por sensor
    from sqlalchemy import func
    subq = (
        select(Reading.sensor_id, func.max(Reading.timestamp).label("max_ts"))
        .group_by(Reading.sensor_id)
        .subquery()
    )
    result = await db.execute(
        select(Reading).join(
            subq,
            (Reading.sensor_id == subq.c.sensor_id) &
            (Reading.timestamp == subq.c.max_ts)
        )
    )
    return result.scalars().all()

@router.get("/{sensor_id}/readings", response_model=List[ReadingResponse])
async def get_sensor_readings(
    sensor_id: int,
    limit: int = Query(100, le=1000),
    from_: Optional[datetime] = Query(None, alias="from"),
    to: Optional[datetime] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Histórico de lecturas de un sensor, con filtros de fecha opcionales."""
    query = (
        select(Reading)
        .where(Reading.sensor_id == sensor_id)
        .order_by(desc(Reading.timestamp))
        .limit(limit)
    )
    if from_:
        query = query.where(Reading.timestamp >= from_)
    if to:
        query = query.where(Reading.timestamp <= to)
    result = await db.execute(query)
    return result.scalars().all()