from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models.threshold import Threshold
from app.schemas.threshold import ThresholdCreate, ThresholdResponse

router = APIRouter(prefix="/thresholds", tags=["Thresholds"])

@router.get("/", response_model=List[ThresholdResponse])
async def get_thresholds(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Threshold))
    return result.scalars().all()

@router.post("/", response_model=ThresholdResponse)
async def create_threshold(threshold_in: ThresholdCreate, db: AsyncSession = Depends(get_db)):
    new_t = Threshold(**threshold_in.model_dump())
    db.add(new_t)
    await db.commit()
    await db.refresh(new_t)
    return new_t