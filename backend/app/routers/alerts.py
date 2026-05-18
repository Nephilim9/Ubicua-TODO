from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from app.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertResponse, AlertUpdate

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/", response_model=List[AlertResponse])
async def list_alerts(status: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Alert).order_by(desc(Alert.created_at))
    if status:
        query = query.where(Alert.status == status)
    result = await db.execute(query)
    return result.scalars().all()

@router.put("/{alert_id}/ack", response_model=AlertResponse)
async def acknowledge_alert(alert_id: int, update: AlertUpdate, db: AsyncSession = Depends(get_db)):
    alert = await db.get(Alert, alert_id)
    alert.status = update.status
    alert.resolved_by = update.resolved_by
    await db.commit()
    await db.refresh(alert)
    return alert