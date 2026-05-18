from app.cache import get_cache, set_cache, delete_cache
from typing import Any, Optional

class CacheService:
    @staticmethod
    async def get_device_status(mac_address: str) -> Optional[str]:
        """Recupera el estado online/offline de un dispositivo desde la caché."""
        return await get_cache(f"status_{mac_address}")

    @staticmethod
    async def set_device_status(mac_address: str, status: str):
        """Guarda el estado del dispositivo (expira en 5 min si no hay reporte)."""
        await set_cache(f"status_{mac_address}", status, ttl=300)

    @staticmethod
    async def cache_thresholds(sensor_type: str, thresholds: list):
        """Almacena los umbrales serializados para evitar consultas a la DB."""
        await set_cache(f"thresholds_{sensor_type}", thresholds, ttl=600)