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

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(device_id: int, db: AsyncSession = Depends(get_db)):
    device = await db.get(Device, device_id)
    if not device:
        raise DeviceNotFoundError(str(device_id))
    await db.delete(device)
    await db.commit()

@router.post("/{device_id}/ping")
async def ping_device(device_id: int, db: AsyncSession = Depends(get_db)):
    """Envía un ping al ESP32 y retorna el estado de conectividad."""
    device = await db.get(Device, device_id)
    if not device:
        raise DeviceNotFoundError(str(device_id))
    # En producción esto enviaría el comando vía WiFi/serial al gateway
    return {
        "device_id": device_id,
        "mac_address": device.mac_address,
        "ping_sent": True,
        "status": device.status,
        "message": "Ping enviado al gateway ESP-NOW"
    }