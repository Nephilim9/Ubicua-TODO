import asyncio
import serial_asyncio
import json
import logging

logger = logging.getLogger(__name__)

class SerialHandler(asyncio.Protocol):
    def __init__(self, callback):
        self.callback = callback
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        logger.info("Puerto serial abierto con el ESP32 Master.")

    def data_received(self, data):
        # El ESP32 envía mensajes terminados en nueva línea (\n)
        lines = data.decode(errors='ignore').split('\n')
        for line in lines:
            if line.strip():
                try:
                    message = json.loads(line)
                    # Pasamos el mensaje al Bridge
                    asyncio.create_task(self.callback(message))
                except json.JSONDecodeError:
                    logger.warning(f"Mensaje serial malformado: {line}")

    def connection_lost(self, exc):
        logger.error("Conexión serial perdida. Reintentando...")