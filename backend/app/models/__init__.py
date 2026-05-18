from app.database import Base
from .device import Device
from .sensor import Sensor
from .reading import Reading
from .threshold import Threshold
from .alert import Alert
from .event_log import EventLog
from .user import User

# Esto permite importar todos los modelos directamente desde app.models
__all__ = [
    "Base", 
    "Device", 
    "Sensor", 
    "Reading", 
    "Threshold", 
    "Alert", 
    "EventLog", 
    "User"
]