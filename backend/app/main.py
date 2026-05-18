import logging
import asyncio
import serial_asyncio
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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- ACCIONES AL INICIAR ---
    logger.info("Iniciando SafeHome Backend...")
    await init_db() # Optimiza SQLite (WAL mode) para la RPi
    
    # Configuración del puerto Serial (USB) para el ESP32 Master
    try:
        loop = asyncio.get_event_loop()
        # El puerto se define en settings (ej: /dev/ttyUSB0)
        transport, protocol = await serial_asyncio.create_serial_connection(
            loop, 
            lambda: SerialHandler(process_esp32_message), 
            settings.ESP32_SERIAL_PORT, 
            baudrate=115200
        )
        logger.info(f"Conexión serial establecida en {settings.ESP32_SERIAL_PORT}")
    except Exception as e:
        logger.error(f"No se pudo abrir el puerto serial: {e}. El sistema operará sin hardware.")

    yield
    # --- ACCIONES AL APAGAR ---
    logger.info("Apagando SafeHome Backend...")

app = FastAPI(
    title="SafeHome ESP-NOW API",
    description=f"Desarrollado por {settings.PROJECT_OWNER}",
    version="1.0.0",
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