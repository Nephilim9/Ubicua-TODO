from sqlalchemy.ext.asyncio import AsyncSession
from app.models.sensor import Sensor
from app.models.reading import Reading

class SensorService:
    @staticmethod
    async def process_reading(db: AsyncSession, sensor_id: int, raw_value: float):
        """
        Aplica procesamiento (calibración) a una lectura cruda antes de guardarla.
        """
        sensor = await db.get(Sensor, sensor_id)
        if not sensor:
            return None
        
        # Ejemplo simple: Si es MQ135, podríamos aplicar una fórmula de calibración
        processed_value = raw_value 
        if sensor.sensor_type == "MQ135":
            # Aquí iría la lógica de conversión ppm
            processed_value = raw_value * 1.1 

        return processed_value