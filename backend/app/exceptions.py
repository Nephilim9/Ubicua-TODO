from fastapi import HTTPException, status

class DeviceNotFoundError(HTTPException):
    def __init__(self, identifier: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Dispositivo '{identifier}' no encontrado en el sistema."
        )

class SensorNotFoundError(HTTPException):
    def __init__(self, sensor_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Sensor con ID '{sensor_id}' no encontrado."
        )

class ConfigurationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Error de configuración: {message}"
        )

class AlertResolutionError(HTTPException):
    def __init__(self, alert_id: int, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            detail=f"No se pudo resolver la alerta {alert_id}: {message}"
        )