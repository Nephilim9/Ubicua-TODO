from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceResponse, DeviceUpdate
from app.exceptions import DeviceNotFoundError

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.get("/", response_model=List[DeviceResponse])
async def list_devices(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Device))
    return result.scalars().all()

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
async def register_device(device_in: DeviceCreate, db: AsyncSession = Depends(get_db)):
    # Verificar si ya existe por MAC
    existing = await db.execute(select(Device).where(Device.mac_address == device_in.mac_address))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="La dirección MAC ya está registrada")
    
    new_device = Device(**device_in.model_dump())
    db.add(new_device)
    await db.commit()
    await db.refresh(new_device)
    return new_device

@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: int, db: AsyncSession = Depends(get_db)):
    device = await db.get(Device, device_id)
    if not device:
        raise DeviceNotFoundError(str(device_id))
    return device

@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: int, device_in: DeviceUpdate, db: AsyncSession = Depends(get_db)):
    device = await db.get(Device, device_id)
    if not device:
        raise DeviceNotFoundError(str(device_id))
    
    update_data = device_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(device, key, value)
    
    await db.commit()
    await db.refresh(device)
    return device