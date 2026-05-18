import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.integration
async def test_create_sensor_and_read_it(db_session):
    """Prueba el flujo: Crear sensor -> Listar sensor vía API."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # 1. Crear un dispositivo primero (requerido por FK)
        dev_res = await ac.post("/api/v1/devices/", json={
            "name": "ESP32-Sala",
            "mac_address": "A1:B2:C3:D4:E5:F6",
            "device_type": "SLAVE"
        })
        device_id = dev_res.json()["id"]

        # 2. Crear el sensor
        sensor_data = {
            "name": "Detector Humo",
            "sensor_type": "MQ135",
            "device_id": device_id,
            "pin_number": 34
        }
        response = await ac.post("/api/v1/sensors/", json=sensor_data)
        
    assert response.status_code == 201
    assert response.json()["name"] == "Detector Humo"
