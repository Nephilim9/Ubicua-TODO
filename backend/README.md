# SafeHome ESP-NOW — Backend

API REST + WebSocket para el sistema de seguridad doméstica ESP-NOW.  
**FastAPI · SQLAlchemy Async · SQLite WAL · Socket.IO**

---

## Estructura interna

```
app/
├── main.py              # Lifespan: init DB, seed, serial, CORS
├── config.py            # Settings via pydantic-settings (.env)
├── database.py          # Motor async SQLite + PRAGMAs WAL
├── seed.py              # Datos de demostración (se ejecuta una vez)
├── dependencies.py      # Dependencias compartidas (API key, DB session)
├── exceptions.py        # Excepciones de dominio personalizadas
│
├── models/              # SQLAlchemy ORM
│   ├── device.py        # Nodo ESP32 (MASTER/SLAVE)
│   ├── sensor.py        # Sensor físico (MQ135/PIR/NFC/TEMP)
│   ├── reading.py       # Lectura de sensor con timestamp
│   ├── threshold.py     # Regla de umbral (GT/LT/EQ + severidad)
│   ├── alert.py         # Evento de alerta generado
│   ├── event_log.py     # Log de eventos del sistema
│   └── user.py          # Usuario del dashboard
│
├── schemas/             # Pydantic v2 — validación request/response
│   ├── device.py
│   ├── sensor.py
│   ├── reading.py
│   ├── threshold.py
│   └── alert.py
│
├── routers/             # Endpoints FastAPI (por recurso)
│   ├── devices.py       # GET/POST/PUT/DELETE /devices
│   ├── sensors.py       # GET/POST/PUT /sensors + /readings
│   ├── alerts.py        # GET/PUT (ack/resolve) /alerts
│   ├── thresholds.py    # GET/POST/PUT/DELETE /thresholds
│   ├── dashboard.py     # GET /dashboard/summary + /chart-data
│   ├── health.py        # GET /health
│   └── websocket.py     # Socket.IO — emit alert_triggered
│
├── services/            # Lógica de negocio
│   ├── sensor_service.py
│   ├── alert_service.py
│   ├── device_comm_service.py
│   ├── cache_service.py
│   └── report_service.py
│
└── core/                # Integración con hardware
    ├── serial_handler.py    # Protocolo JSON line-delimited (TCP/serial)
    ├── esp32_bridge.py      # Parseo y ruteo de mensajes del gateway
    └── alert_engine.py      # Motor de evaluación de umbrales
```

---

## Instalación

```bash
# Requiere uv (https://docs.astral.sh/uv/)
uv sync

# Arrancar en desarrollo
uv run uvicorn app.main:app --reload --port 8000

# Arrancar en producción (RPi 3B+)
uv run uvicorn app.main:app \
  --host 0.0.0.0 --port 8000 \
  --workers 1 --limit-concurrency 50 --timeout-keep-alive 5
```

Al arrancar, el backend ejecuta automáticamente:

1. `os.makedirs("data", exist_ok=True)` — crea el directorio de la BD
2. `Base.metadata.create_all(engine)` — crea tablas si no existen
3. PRAGMAs de optimización SQLite (WAL, cache 32 MB, foreign_keys ON)
4. `seed_if_empty()` — carga datos de demo si la BD está vacía
5. Intento de conexión serial al gateway ESP32 (falla silenciosa si no hay hardware)

---

## Configuración (`.env`)

| Variable | Default | Descripción |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite+aiosqlite:///data/sistema_seguridad.db` | URL de la base de datos |
| `ESP32_SERIAL_PORT` | `COM3` | Puerto serial del gateway ESP32 |
| `ESP32_BAUD_RATE` | `115200` | Velocidad de comunicación serial |
| `SQLITE_JOURNAL_MODE` | `WAL` | Modo WAL para concurrencia |
| `SQLITE_CACHE_SIZE` | `-32000` | Cache SQLite (32 MB en RAM) |
| `JWT_SECRET` | *(cambiar)* | Clave para tokens JWT del dashboard |
| `ESP32_SECRET_KEY` | *(cambiar)* | API Key compartida con firmware ESP32 |
| `CACHE_PATH` | `cache/sistema_seguridad.cache` | Path del caché diskcache |
| `DB_RETENTION_DAYS` | `30` | Días de retención de lecturas |

---

## Protocolo de Mensajes ESP32

El gateway envía mensajes JSON por línea (JSON line-delimited) al backend:

### Lectura de sensor

```json
{
  "type": "sensor_reading",
  "device_mac": "A4:CF:12:34:56:78",
  "sensor_type": "MQ135",
  "value": 423.5,
  "timestamp": 1716000000
}
```

### Estado de dispositivo

```json
{
  "type": "device_status",
  "device_mac": "B4:CF:12:34:56:79",
  "status": "online",
  "rssi": -62
}
```

### Evento NFC

```json
{
  "type": "nfc_event",
  "device_mac": "A4:CF:12:34:56:78",
  "uid": "04:A3:B2:C1",
  "authorized": true
}
```

---

## Base de Datos

**SQLite en modo WAL** — optimizado para escrituras frecuentes y concurrencia en RPi:

```
Device (1) ──────── (N) Sensor (1) ──────── (N) Reading
                         │
                         └── sensor_type ──► Threshold (1) ─── (N) Alert
```

### Optimizaciones RPi 3B+

```sql
PRAGMA journal_mode = WAL;       -- Escritura sin bloquear lecturas
PRAGMA synchronous = NORMAL;     -- Balance seguridad/velocidad
PRAGMA cache_size = -32000;      -- 32 MB de cache en RAM
PRAGMA foreign_keys = ON;        -- Integridad referencial
```

---

## Tests

```bash
# Suite completa
uv run pytest

# Por marcador
uv run pytest -m unit           # Lógica pura (sin I/O)
uv run pytest -m integration    # Endpoints + DB en memoria
uv run pytest -m e2e            # Flujo completo

# Cobertura
uv run pytest --cov=app --cov-report=term-missing
```

### Estructura de tests

```
tests/
├── unit/
│   ├── test_alert_engine.py    # Lógica de evaluación de umbrales
│   ├── test_cache.py           # TTL del caché
│   └── test_services.py        # Calibración, formato de comandos
├── integration/
│   ├── test_api_sensors.py     # Crear sensor → listar vía API
│   ├── test_api_alerts.py      # CRUD alertas
│   └── test_websocket.py       # Emisión de eventos Socket.IO
└── e2e/
    └── test_full_flow.py       # ESP32 msg → DB → alert
```

---

## Docker (Raspberry Pi)

```bash
# En la RPi
docker compose up -d

# Límites de recursos configurados en docker-compose.yml:
#   memory: 400M  (deja 600 MB libres para el SO)
#   privileged: true  (acceso a /dev/ttyUSB0)
```

El `Dockerfile` usa `python:3.11-slim-bookworm` para mínima huella en ARM.
