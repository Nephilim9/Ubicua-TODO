"""
seed.py — Datos de demostración para SafeHome ESP-NOW.

Se ejecuta una sola vez al arrancar si la base de datos está vacía.
Útil para desarrollo y para que el frontend tenga datos que mostrar
sin necesidad de hardware físico.
"""
import logging
from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal
from app.models.device import Device
from app.models.sensor import Sensor
from app.models.reading import Reading
from app.models.threshold import Threshold
from app.models.alert import Alert

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Dispositivos de demostración — reflejan la arquitectura ESP-NOW real:
#   ESP-Master Gateway = baquela con ESP-NOW + ESP-WiFi bridge
#   ESP-Nodo-0x = nodos esclavos con sensores físicos
# ---------------------------------------------------------------------------
DEMO_DEVICES = [
    {
        "mac_address": "A4:CF:12:34:56:78",
        "name": "ESP-Gateway (Cocina)",
        "location": "Cocina",
        "device_type": "MASTER",
        "status": "online",
        "firmware_version": "1.2.0",
    },
    {
        "mac_address": "B4:CF:12:34:56:79",
        "name": "ESP-Nodo-01 (Sala)",
        "location": "Sala",
        "device_type": "SLAVE",
        "status": "online",
        "firmware_version": "1.1.0",
    },
    {
        "mac_address": "C4:CF:12:34:56:80",
        "name": "ESP-Nodo-02 (Garage)",
        "location": "Garage",
        "device_type": "SLAVE",
        "status": "offline",
        "firmware_version": "1.0.5",
    },
    {
        "mac_address": "D4:CF:12:34:56:81",
        "name": "ESP-Nodo-03 (Dormitorio)",
        "location": "Dormitorio",
        "device_type": "SLAVE",
        "status": "online",
        "firmware_version": "1.1.0",
    },
]

DEMO_SENSORS = [
    # Gateway
    {"device_index": 0, "sensor_type": "MQ135", "name": "Sensor Gas Cocina",      "unit": "ppm",     "pin_number": 34},
    {"device_index": 0, "sensor_type": "PIR",   "name": "PIR Cocina",              "unit": "bool",    "pin_number": 25},
    {"device_index": 0, "sensor_type": "NFC",   "name": "Lector NFC Entrada",      "unit": "uid",     "pin_number": 21},
    # Sala
    {"device_index": 1, "sensor_type": "MQ135", "name": "Sensor Gas Sala",         "unit": "ppm",     "pin_number": 34},
    {"device_index": 1, "sensor_type": "PIR",   "name": "PIR Sala",                "unit": "bool",    "pin_number": 25},
    # Garage
    {"device_index": 2, "sensor_type": "PIR",   "name": "PIR Garage",              "unit": "bool",    "pin_number": 25},
    # Dormitorio
    {"device_index": 3, "sensor_type": "MQ135", "name": "Sensor Gas Dormitorio",   "unit": "ppm",     "pin_number": 34},
    {"device_index": 3, "sensor_type": "PIR",   "name": "PIR Dormitorio",          "unit": "bool",    "pin_number": 25},
]

DEMO_THRESHOLDS = [
    {
        "sensor_type": "MQ135",
        "name": "Gas — Advertencia",
        "operator": "GT",
        "value_max": 400.0,
        "severity": "MEDIUM",
        "notification_channels": '["ws","buzzer"]',
    },
    {
        "sensor_type": "MQ135",
        "name": "Gas — Crítico (fuga)",
        "operator": "GT",
        "value_max": 600.0,
        "severity": "CRITICAL",
        "notification_channels": '["ws","buzzer","led"]',
    },
    {
        "sensor_type": "PIR",
        "name": "Movimiento detectado",
        "operator": "GT",
        "value_max": 0.5,
        "severity": "HIGH",
        "notification_channels": '["ws"]',
    },
]


async def seed_if_empty() -> None:
    """Inserta datos de demo sólo si la tabla devices está vacía."""
    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(Device).limit(1))
        if existing.scalar_one_or_none():
            logger.info("Base de datos ya tiene datos — seed omitido.")
            return

        logger.info("Base de datos vacía — cargando datos de demostración...")
        await _seed(db)
        logger.info("Seed completado exitosamente.")


async def _seed(db: AsyncSession) -> None:
    now = datetime.utcnow()

    # 1. Dispositivos
    devices: list[Device] = []
    for d in DEMO_DEVICES:
        dev = Device(
            **d,
            last_seen=now if d["status"] == "online" else now - timedelta(hours=3),
            created_at=now - timedelta(days=7),
        )
        db.add(dev)
        devices.append(dev)
    await db.flush()  # Obtiene IDs sin commit

    # 2. Sensores
    sensors: list[Sensor] = []
    for s in DEMO_SENSORS:
        device_id = devices[s["device_index"]].id
        sensor = Sensor(
            device_id=device_id,
            sensor_type=s["sensor_type"],
            name=s["name"],
            unit=s["unit"],
            pin_number=s["pin_number"],
            is_active=True,
        )
        db.add(sensor)
        sensors.append(sensor)
    await db.flush()

    # 3. Umbrales
    thresholds: list[Threshold] = []
    for t in DEMO_THRESHOLDS:
        thr = Threshold(**t, is_active=True)
        db.add(thr)
        thresholds.append(thr)
    await db.flush()

    # 4. Lecturas históricas (últimas 6 horas, cada 5 minutos)
    import random
    mq135_sensors = [s for s in sensors if s.sensor_type == "MQ135"]
    pir_sensors   = [s for s in sensors if s.sensor_type == "PIR"]

    for minutes_ago in range(360, 0, -5):
        ts = now - timedelta(minutes=minutes_ago)
        for sensor in mq135_sensors:
            base = 280 + random.gauss(0, 40)
            # Simular pico a las 2h atrás
            if 100 < minutes_ago < 130:
                base += 350
            value = max(100.0, round(base, 1))
            db.add(Reading(
                sensor_id=sensor.id,
                device_id=sensor.device_id,
                value=value,
                value_processed=round(value * 1.05, 1),
                timestamp=ts,
            ))
        for sensor in pir_sensors:
            # PIR activo esporádicamente
            value = 1.0 if random.random() < 0.08 else 0.0
            db.add(Reading(
                sensor_id=sensor.id,
                device_id=sensor.device_id,
                value=value,
                value_processed=value,
                timestamp=ts,
            ))

    await db.flush()

    # 5. Alertas de ejemplo
    mq_sensor   = mq135_sensors[0]
    crit_thresh = thresholds[1]  # CRITICAL > 600

    alerts_data = [
        {
            "sensor_id":       mq_sensor.id,
            "device_id":       mq_sensor.device_id,
            "threshold_id":    crit_thresh.id,
            "severity":        "CRITICAL",
            "message":         "Gas > 600 ppm — Posible fuga detectada en Cocina",
            "value_triggered": 720.0,
            "status":          "resolved",
            "resolved_by":     "admin",
            "resolved_at":     now - timedelta(hours=1, minutes=45),
            "created_at":      now - timedelta(hours=2),
        },
        {
            "sensor_id":       mq_sensor.id,
            "device_id":       mq_sensor.device_id,
            "threshold_id":    thresholds[0].id,
            "severity":        "MEDIUM",
            "message":         "Gas > 400 ppm — Nivel elevado en Cocina",
            "value_triggered": 450.0,
            "status":          "acknowledged",
            "created_at":      now - timedelta(hours=1),
        },
        {
            "sensor_id":       pir_sensors[0].id,
            "device_id":       pir_sensors[0].device_id,
            "threshold_id":    thresholds[2].id,
            "severity":        "HIGH",
            "message":         "Movimiento detectado en Sala",
            "value_triggered": 1.0,
            "status":          "active",
            "created_at":      now - timedelta(minutes=20),
        },
    ]

    for a in alerts_data:
        db.add(Alert(**a))

    await db.commit()
