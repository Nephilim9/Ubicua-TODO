from app.services.sensor_service import SensorService
from app.services.alert_service import AlertService
from app.database import AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)

async def process_esp32_message(message: dict):
    """
    Orquestador de mensajes provenientes del hardware.
    """
    msg_type = message.get("type")
    
    async with AsyncSessionLocal() as db:
        if msg_type == "sensor_reading":
            # Lógica para procesar y guardar la lectura
            # Aquí conectaríamos con SensorService y AlertService
            logger.info(f"Lectura recibida: {message}")
            
        elif msg_type == "nfc_auth":
            logger.info(f"Intento de acceso NFC: {message.get('nfc_uid')}")
            
        elif msg_type == "pong":
            logger.debug(f"Dispositivo activo: {message.get('device_mac')}")