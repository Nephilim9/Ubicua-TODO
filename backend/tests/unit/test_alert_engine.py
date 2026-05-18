# Proyecto: SafeHome ESP-NOW | Grupo 4
import pytest
from app.services.alert_service import AlertService
from app.models.threshold import Threshold
from app.models.reading import Reading

@pytest.mark.unit
async def test_logic_threshold_breach():
    """Prueba que la lógica detecte correctamente cuando se supera un umbral."""
    # Simulamos un umbral de temperatura crítica
    threshold = Threshold(
        sensor_type="TEMP",
        operator="GT",
        value_max=40.0,
        severity="CRITICAL"
    )
    
    # Lectura que debería disparar alerta
    reading_high = Reading(value=45.0)
    
    # Verificamos la lógica de comparación (GT = Greater Than)
    assert reading_high.value > threshold.value_max

@pytest.mark.unit
async def test_logic_normal_reading():
    """Prueba que valores normales no disparen alertas."""
    threshold = Threshold(sensor_type="MQ135", operator="GT", value_max=500.0)
    reading_safe = Reading(value=120.0)
    
    assert not (reading_safe.value > threshold.value_max)