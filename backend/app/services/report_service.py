from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.reading import Reading
from datetime import datetime, timedelta

class ReportService:
    @staticmethod
    async def get_daily_average(db: AsyncSession, sensor_id: int):
        """Calcula el promedio de lecturas de las últimas 24 horas."""
        yesterday = datetime.now() - timedelta(days=1)
        query = select(func.avg(Reading.value)).where(
            Reading.sensor_id == sensor_id,
            Reading.timestamp >= yesterday
        )
        result = await db.execute(query)
        return result.scalar() or 0.0

    @staticmethod
    async def get_alert_summary(db: AsyncSession, days: int = 7):
        """Genera un resumen de alertas por severidad."""
        # Esta lógica se expandirá para generar archivos CSV/JSON
        pass