import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings

logger = logging.getLogger(__name__)

# Configuración del motor asíncrono para SQLite
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={
        "timeout": settings.SQLITE_TIMEOUT,
        "check_same_thread": False,
    }
)

# Sesión asíncrona
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def init_db():
    """Ejecuta PRAGMAs para optimizar SQLite en la Raspberry Pi."""
    async with engine.begin() as conn:
        await conn.execute(f"PRAGMA journal_mode={settings.SQLITE_JOURNAL_MODE}")
        await conn.execute(f"PRAGMA synchronous={settings.SQLITE_SYNCHRONOUS}")
        await conn.execute(f"PRAGMA cache_size={settings.SQLITE_CACHE_SIZE}")

async def get_db():
    """Dependencia para inyectar la sesión de base de datos en FastAPI."""
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()