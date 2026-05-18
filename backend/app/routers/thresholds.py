from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models.threshold import Threshold
from app.schemas.threshold import ThresholdCreate, ThresholdUpdate, ThresholdResponse

router = APIRouter(prefix="/thresholds", tags=["Thresholds"])

@router.get("/", response_model=List[ThresholdResponse])
async def get_thresholds(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Threshold))
    return result.scalars().all()

@router.post("/", response_model=ThresholdResponse, status_code=status.HTTP_201_CREATED)
async def create_threshold(threshold_in: ThresholdCreate, db: AsyncSession = Depends(get_db)):
    new_t = Threshold(**threshold_in.model_dump())
    db.add(new_t)
    await db.commit()
    await db.refresh(new_t)
    return new_t

@router.get("/{threshold_id}", response_model=ThresholdResponse)
async def get_threshold(threshold_id: int, db: AsyncSession = Depends(get_db)):
    t = await db.get(Threshold, threshold_id)
    if not t:
        raise HTTPException(status_code=404, detail=f"Umbral {threshold_id} no encontrado")
    return t

@router.put("/{threshold_id}", response_model=ThresholdResponse)
async def update_threshold(threshold_id: int, threshold_in: ThresholdUpdate, db: AsyncSession = Depends(get_db)):
    t = await db.get(Threshold, threshold_id)
    if not t:
        raise HTTPException(status_code=404, detail=f"Umbral {threshold_id} no encontrado")
    for key, value in threshold_in.model_dump(exclude_unset=True).items():
        setattr(t, key, value)
    await db.commit()
    await db.refresh(t)
    return t

@router.delete("/{threshold_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_threshold(threshold_id: int, db: AsyncSession = Depends(get_db)):
    t = await db.get(Threshold, threshold_id)
    if not t:
        raise HTTPException(status_code=404, detail=f"Umbral {threshold_id} no encontrado")
    await db.delete(t)
    await db.commit()