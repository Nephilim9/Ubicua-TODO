from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.config import settings

# Configuración de lectura del header para la API Key
api_key_header = APIKeyHeader(name=settings.API_KEY_HEADER, auto_error=False)

async def verify_esp32_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Dependencia para validar que los datos entrantes provienen de un ESP32 autorizado.
    """
    if not api_key or api_key != settings.ESP32_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Credenciales de dispositivo inválidas o ausentes",
        )
    return api_key

# Dependencia alias para mantener el código limpio en los routers
# Permite usar SessionDep = Depends(get_database_session)
async def get_database_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db