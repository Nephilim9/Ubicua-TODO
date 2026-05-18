from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from app.database import get_db
from app.models.sensor import Sensor
from app.models.reading import Reading
from app.schemas.sensor import SensorCreate, SensorResponse, SensorUpdate
from app.schemas.reading import ReadingCreate, ReadingResponse
from app.dependencies import verify_esp32_api_key
from app.exceptions import SensorNotFoundError

router = APIRouter(prefix="/sensors", tags=["Sensors"])

# --- Endpoints de CRUD Sensores ---
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

# --- Endpoints de Lecturas (según prompt estructurado) ---
@router.post("/readings", response_model=ReadingResponse, dependencies=[Depends(verify_esp32_api_key)])
async def post_reading(reading_in: ReadingCreate, db: AsyncSession = Depends(get_db)):
    new_reading = Reading(**reading_in.model_dump())
    db.add(new_reading)
    await db.commit()
    await db.refresh(new_reading)
    return new_reading

@router.get("/{sensor_id}/readings", response_model=List[ReadingResponse])
async def get_sensor_readings(
    sensor_id: int, 
    limit: int = Query(50, le=500), 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Reading).where(Reading.sensor_id == sensor_id)
        .order_by(desc(Reading.timestamp)).limit(limit)
    )
    return result.scalars().all()