import json
from datetime import datetime
from app.models.device import Device

class DeviceCommService:
    @staticmethod
    async def send_command(device: Device, cmd_type: str, payload: dict = None):
        """
        Prepara el JSON para ser enviado vía Serial o WiFi al ESP32 Master.
        """
        command = {
            "type": cmd_type,
            "target_mac": device.mac_address,
            "payload": payload or {},
            "timestamp": int(datetime.now().timestamp())
        }
        
        # En una fase posterior, el SerialHandler (en core/) 
        # tomará este string para enviarlo físicamente.
        return json.dumps(command)