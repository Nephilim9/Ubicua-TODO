from app.database import Base
from app.models import Device, Sensor, Reading, Threshold, Alert, EventLog, User

# Importante: Alembic necesita ver los metadatos de tus modelos
target_metadata = Base.metadata