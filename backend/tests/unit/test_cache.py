# Proyecto: SafeHome ESP-NOW | Grupo 4
import pytest
import asyncio
from app.cache import set_cache, get_cache

@pytest.mark.unit
async def test_cache_expiration():
    """Prueba que el TTL (tiempo de vida) de la caché funcione."""
    await set_cache("test_key", "valor_temporal", ttl=1)
    
    # Inmediatamente debe existir
    val = await get_cache("test_key")
    assert val == "valor_temporal"
    
    # Esperamos a que expire
    await asyncio.sleep(1.1)
    val_expirado = await get_cache("test_key")
    assert val_expirado is None