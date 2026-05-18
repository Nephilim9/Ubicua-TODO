# Proyecto: SafeHome ESP-NOW | Grupo 4
import asyncio
from app.services.alert_service import AlertService

class AlertEngine:
    """
    Motor encargado de disparar evaluaciones masivas o limpiezas de alertas.
    """
    def __init__(self):
        self.is_running = False

    async def start(self):
        self.is_running = True
        logger.info("Motor de evaluación de umbrales iniciado.")

    async def stop(self):
        self.is_running = False