from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from app.models.alert import Alert
from app.models.threshold import Threshold
from app.models.reading import Reading
from app.cache import get_cache, set_cache
from app.routers.websocket import broadcast_alert

class AlertService:
    @staticmethod
    async def evaluate_reading(db: AsyncSession, reading: Reading):
        """
        Evalúa una nueva lectura contra los umbrales configurados.
        """
        # 1. Intentar obtener umbrales desde caché para ahorrar recursos en RPi
        cache_key = f"thresholds_{reading.sensor.sensor_type}"
        thresholds = await get_cache(cache_key)

        if not thresholds:
            result = await db.execute(
                select(Threshold).where(
                    Threshold.sensor_type == reading.sensor.sensor_type,
                    Threshold.is_active == True
                )
            )
            thresholds = result.scalars().all()
            # Guardar en caché por 5 minutos
            # Nota: Necesitarías serializar a dict si usas el cache.py anterior
            # Para este ejemplo, asumimos la lógica de evaluación directa:

        for t in thresholds:
            triggered = False
            val = reading.value
            
            if t.operator == "GT" and val > t.value_max: triggered = True
            elif t.operator == "LT" and val < t.value_min: triggered = True
            elif t.operator == "BETWEEN" and t.value_min <= val <= t.value_max: triggered = True

            if triggered:
                # 2. Verificar Cooldown (Deduplicación)
                dedup_key = f"alert_cooldown_{reading.sensor_id}_{t.id}"
                if await get_cache(dedup_key):
                    continue # Saltar si ya se emitió alerta recientemente

                # 3. Crear Alerta en DB
                new_alert = Alert(
                    sensor_id=reading.sensor_id,
                    device_id=reading.device_id,
                    threshold_id=t.id,
                    severity=t.severity,
                    message=f"Alerta {t.name}: Valor {val} detectado",
                    value_triggered=val
                )
                db.add(new_alert)
                await db.commit()

                # 4. Notificar vía WebSocket en tiempo real
                await broadcast_alert({
                    "type": "alert.triggered",
                    "severity": t.severity,
                    "message": new_alert.message,
                    "sensor": reading.sensor.name
                })

                # 5. Activar Cooldown (ej: 60 segundos)
                await set_cache(dedup_key, "active", ttl=60)