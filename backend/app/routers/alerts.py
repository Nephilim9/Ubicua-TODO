from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from typing import List, Optional
from app.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertResponse, AlertUpdate

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/", response_model=List[AlertResponse])
async def list_alerts(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    query = select(Alert).order_by(desc(Alert.created_at)).limit(limit)
    if status:
        query = query.where(Alert.status == status)
    if severity:
        query = query.where(Alert.severity == severity)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/stats")
async def alert_stats(db: AsyncSession = Depends(get_db)):
    """Estadísticas de alertas agrupadas por severidad y estado."""
    by_severity = await db.execute(
        select(Alert.severity, func.count(Alert.id))
        .group_by(Alert.severity)
    )
    by_status = await db.execute(
        select(Alert.status, func.count(Alert.id))
        .group_by(Alert.status)
    )
    return {
        "by_severity": dict(by_severity.all()),
        "by_status":   dict(by_status.all()),
    }

@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    alert = await db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alerta {alert_id} no encontrada")
    return alert

@router.put("/{alert_id}/ack", response_model=AlertResponse)
async def acknowledge_alert(alert_id: int, update: AlertUpdate, db: AsyncSession = Depends(get_db)):
    """Reconocer una alerta activa."""
    alert = await db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alerta {alert_id} no encontrada")
    alert.status = "acknowledged"
    alert.resolved_by = update.resolved_by
    await db.commit()
    await db.refresh(alert)
    return alert

@router.put("/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(alert_id: int, update: AlertUpdate, db: AsyncSession = Depends(get_db)):
    """Marcar una alerta como resuelta."""
    alert = await db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"Alerta {alert_id} no encontrada")
    alert.status = "resolved"
    alert.resolved_by = update.resolved_by
    alert.resolved_at = datetime.utcnow()
    await db.commit()
    await db.refresh(alert)
    return alert