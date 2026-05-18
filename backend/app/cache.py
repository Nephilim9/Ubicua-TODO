import diskcache as dc
import json
from typing import Any, Optional
from app.config import settings


cache_db = dc.Cache(
    settings.CACHE_PATH, 
    size_limit=settings.CACHE_MAX_SIZE_MB * 1024 * 1024
)

async def set_cache(key: str, value: Any, ttl: int = settings.DEFAULT_TTL) -> None:
    """Guarda un valor en caché con un tiempo de vida (TTL) en segundos."""
    cache_db.set(key, json.dumps(value), expire=ttl)

async def get_cache(key: str) -> Optional[Any]:
    """Recupera un valor de la caché si existe y no ha expirado."""
    value = cache_db.get(key)
    if value is not None:
        return json.loads(value)
    return None

async def delete_cache(key: str) -> None:
    """Elimina un valor específico de la caché."""
    cache_db.delete(key)

async def clear_cache() -> None:
    """Limpia toda la caché (útil cuando se actualizan configuraciones globales)."""
    cache_db.clear()