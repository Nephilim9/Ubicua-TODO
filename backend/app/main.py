import os
import logging
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Importación de routers
from app.routers import (
    devices,
    sensors,
    alerts,
    thresholds,
    dashboard,
    health,
    websocket
)
from app.database import init_db
from app.config import settings
from app.core.serial_handler import SerialHandler
from app.core.esp32_bridge import process_esp32_message

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- ACCIONES AL INICIAR ---
    logger.info("Iniciando SafeHome Backend...")

    # Crear directorios necesarios si no existen
    os.makedirs("data", exist_ok=True)
    os.makedirs("cache", exist_ok=True)
    logger.info("Directorios data/ y cache/ verificados.")

    await init_db()  # Crea tablas y optimiza SQLite (WAL mode) para la RPi

    # Seed de datos de demostración (sólo si la BD está vacía)
    try:
        from app.seed import seed_if_empty
        await seed_if_empty()
    except Exception as e:
        logger.warning(f"Seed omitido: {e}")

    # Configuración del puerto Serial (USB) para el ESP32 Master
    try:
        import serial_asyncio
        loop = asyncio.get_event_loop()
        transport, protocol = await serial_asyncio.create_serial_connection(
            loop,
            lambda: SerialHandler(process_esp32_message),
            settings.ESP32_SERIAL_PORT,
            baudrate=settings.ESP32_BAUD_RATE
        )
        logger.info(f"Conexión serial establecida en {settings.ESP32_SERIAL_PORT}")
    except Exception as e:
        logger.warning(
            f"Puerto serial '{settings.ESP32_SERIAL_PORT}' no disponible: {e}. "
            "El sistema operará en modo simulación (sin hardware ESP32)."
        )

    yield
    # --- ACCIONES AL APAGAR ---
    logger.info("Apagando SafeHome Backend...")

app = FastAPI(
    title="SafeHome ESP-NOW API",
    description=f"Sistema de seguridad doméstica IoT | {settings.PROJECT_OWNER}",
    version=settings.VERSION,
    lifespan=lifespan
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Routers
app.include_router(devices.router, prefix="/api/v1")
app.include_router(sensors.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")
app.include_router(thresholds.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")

# Integración de WebSocket para tiempo real
app.mount("/ws", websocket.sio_app)