# SafeHome ESP-NOW 🛡️

**Sistema de Seguridad Doméstica IoT — Dashboard de Monitoreo**  
Desarrollado por **Grupo 4** · Ingeniería en Sistemas / Cómputo Ubicuo

---

## 📋 Descripción

SafeHome ESP-NOW es una aplicación web *fullstack* para monitorear, configurar y gestionar un sistema de seguridad doméstica basado en microcontroladores **ESP32** interconectados mediante el protocolo **ESP-NOW**.

El sistema detecta condiciones de riesgo en tiempo real:
- 🔥 **Humo / Gases** — sensores MQ135
- 🚶 **Movimiento** — sensores PIR
- 🔑 **Autenticación** — módulo NFC

Y está optimizado para desplegarse en una **Raspberry Pi 3B+** (1 GB RAM).

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                      Raspberry Pi 3B+                       │
│  ┌─────────────────────┐    ┌───────────────────────────┐  │
│  │   Backend FastAPI   │◄──►│   Frontend React / Vite   │  │
│  │   SQLite (WAL)      │    │   Tailwind CSS             │  │
│  │   :8000             │    │   :5173                    │  │
│  └──────────┬──────────┘    └───────────────────────────┘  │
│             │ TCP / WiFi                                     │
└─────────────┼───────────────────────────────────────────────┘
              │
    ┌─────────▼──────────┐
    │  Baquela Gateway   │  ← PCB con 2 ESP32
    │  ESP32-A: ESP-NOW  │  ← Recibe datos de nodos esclavos
    │  ESP32-B: WiFi     │  ← Reenvía a la RPi vía TCP
    └─────────┬──────────┘
              │ ESP-NOW (2.4 GHz)
    ┌─────────┼──────────────────────┐
    │         │                      │
    ▼         ▼                      ▼
 Nodo-01   Nodo-02              Nodo-N
 MQ135     MQ135 + PIR          PIR + NFC
 PIR
```

### Flujo de datos

1. Los **nodos ESP32 esclavos** capturan lecturas de sensores y las envían vía **ESP-NOW**
2. El **ESP32-A del gateway** recibe todos los mensajes ESP-NOW y los pasa por UART al **ESP32-B**
3. El **ESP32-B** los reenvía al backend de la RPi vía **TCP/WiFi** (JSON line-delimited)
4. El **backend FastAPI** procesa el mensaje, evalúa umbrales y genera alertas si corresponde
5. Las alertas se emiten en tiempo real al frontend via **Socket.IO WebSocket**

---

## 🗂️ Estructura del Proyecto

```
Ubicua-TODO/
├── backend/                    # FastAPI + SQLAlchemy async
│   ├── app/
│   │   ├── core/               # Lógica de negocio central
│   │   │   ├── serial_handler.py   # Recepción de mensajes TCP/Serial
│   │   │   ├── esp32_bridge.py     # Parseo y ruteo de mensajes ESP32
│   │   │   └── alert_engine.py     # Motor de evaluación de umbrales
│   │   ├── routers/            # Endpoints REST API
│   │   │   ├── devices.py      # CRUD dispositivos ESP32
│   │   │   ├── sensors.py      # CRUD sensores + lecturas
│   │   │   ├── alerts.py       # Gestión de alertas
│   │   │   ├── thresholds.py   # Configuración de umbrales
│   │   │   ├── dashboard.py    # KPIs + datos para gráficos
│   │   │   ├── health.py       # Health check
│   │   │   └── websocket.py    # Socket.IO para tiempo real
│   │   ├── models/             # Modelos SQLAlchemy (ORM)
│   │   ├── schemas/            # Schemas Pydantic (validación)
│   │   ├── services/           # Servicios de negocio
│   │   ├── config.py           # Configuración global (pydantic-settings)
│   │   ├── database.py         # Motor async SQLite + WAL
│   │   ├── main.py             # Punto de entrada FastAPI
│   │   └── seed.py             # Datos de demostración
│   ├── migrations/             # Alembic
│   ├── tests/
│   │   ├── unit/               # Tests unitarios (sin DB)
│   │   ├── integration/        # Tests de integración (API + DB)
│   │   └── e2e/                # Tests de flujo completo
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── dockerfile
│
├── frontend/                   # React 18 + Vite + Tailwind CSS
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/         # Sidebar, Header, Layout
│   │   │   ├── dashboard/      # KPIGrid, SensorChart, AlertFeed, DeviceStatus
│   │   │   ├── alerts/         # AlertList, AlertFilters, AlertDetail
│   │   │   ├── sensors/        # SensorList, ReadingHistory, CalibrationForm
│   │   │   ├── devices/        # DeviceCard, DeviceList, DeviceLogs
│   │   │   └── threshold/      # ThresholdList, ThresholdEditor
│   │   ├── hooks/              # React Query hooks (useAlerts, useDevices…)
│   │   ├── pages/              # Páginas por ruta
│   │   ├── services/           # API client (axios) + WebSocket
│   │   ├── stores/             # Zustand stores
│   │   └── types/              # Interfaces TypeScript
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.ts
│
├── .gitignore
└── README.md                   ← este archivo
```

---

## 🚀 Inicio Rápido (Desarrollo Local)

### Prerrequisitos

| Herramienta | Versión mínima | Uso |
|-------------|---------------|-----|
| Python | 3.11+ | Backend |
| [uv](https://docs.astral.sh/uv/) | 0.4+ | Gestor de paquetes Python |
| Node.js | 18+ | Frontend |
| npm | 9+ | Gestor de paquetes Node |

### 1. Clonar el repositorio

```bash
git clone https://github.com/LNieto-V/Ubicua-TODO.git
cd Ubicua-TODO
```

### 2. Backend

```bash
cd backend

# Instalar dependencias con uv
uv sync

# (Opcional) Copiar y configurar variables de entorno
cp .env.example .env   # editar si es necesario

# Arrancar el servidor
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El servidor crea automáticamente:
- El directorio `data/` y la base de datos SQLite
- Los datos de demostración (seed) si la BD está vacía

📖 **Swagger UI:** http://localhost:8000/docs  
📖 **ReDoc:**       http://localhost:8000/redoc

### 3. Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Arrancar servidor de desarrollo
npm run dev
```

🌐 **Dashboard:** http://localhost:5173

---

## ⚙️ Variables de Entorno

Crea `backend/.env` (copia de `.env.example`) para sobreescribir los defaults:

```env
# Base de datos
DATABASE_URL=sqlite+aiosqlite:///data/sistema_seguridad.db

# Puerto serial del gateway ESP32
# Windows (desarrollo): COM3
# Raspberry Pi:         /dev/ttyUSB0
ESP32_SERIAL_PORT=/dev/ttyUSB0
ESP32_BAUD_RATE=115200

# Seguridad
JWT_SECRET=cambiar-en-produccion-por-clave-segura
ESP32_SECRET_KEY=clave-compartida-con-firmware-esp32
```

---

## 📡 API Reference

Base URL: `http://<host>:8000/api/v1`

### Dashboard

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/dashboard/summary` | KPIs: sensores activos, alertas, nodos, calidad aire |
| `GET` | `/dashboard/chart-data?sensor_type=MQ135&hours=6` | Series de tiempo para gráficos |

### Dispositivos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/devices/` | Listar todos los nodos ESP32 |
| `POST` | `/devices/` | Registrar nuevo dispositivo |
| `GET` | `/devices/{id}` | Detalle de dispositivo |
| `PUT` | `/devices/{id}` | Actualizar dispositivo |
| `DELETE` | `/devices/{id}` | Eliminar dispositivo |
| `POST` | `/devices/{id}/ping` | Enviar ping al gateway |

### Sensores y Lecturas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/sensors/` | Listar sensores |
| `POST` | `/sensors/` | Registrar sensor |
| `GET` | `/sensors/{id}` | Detalle de sensor |
| `GET` | `/sensors/readings/latest` | Última lectura por sensor |
| `GET` | `/sensors/{id}/readings` | Histórico de lecturas |
| `POST` | `/sensors/readings` | Ingestar lectura (requiere API Key) |

### Alertas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/alerts/` | Listar alertas (filtros: status, severity) |
| `GET` | `/alerts/stats` | Conteo por severidad y estado |
| `GET` | `/alerts/{id}` | Detalle de alerta |
| `PUT` | `/alerts/{id}/ack` | Reconocer alerta |
| `PUT` | `/alerts/{id}/resolve` | Marcar como resuelta |

### Umbrales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/thresholds/` | Listar reglas de umbral |
| `POST` | `/thresholds/` | Crear nueva regla |
| `PUT` | `/thresholds/{id}` | Actualizar regla |
| `DELETE` | `/thresholds/{id}` | Eliminar regla |

### WebSocket (Tiempo Real)

```
ws://<host>:8000/ws/socket.io
```

Evento a escuchar: `alert_triggered`  
Payload:
```json
{
  "message": "Gas > 600 ppm — Posible fuga detectada",
  "severity": "CRITICAL",
  "sensor_id": 1,
  "device_mac": "A4:CF:12:34:56:78"
}
```

---

## 🗃️ Modelos de Datos

```
Device          → Sensor         → Reading
(ESP32 nodo)      (MQ135/PIR/NFC)  (lecturas históricas)
     │
     └──────────→ Alert           ← Threshold
                  (evento de        (regla de umbral)
                   seguridad)
```

### Severidades de Alerta

| Nivel | Significado | Ejemplo |
|-------|-------------|---------|
| `CRITICAL` | Riesgo inmediato | Gas > 600 ppm |
| `HIGH` | Situación seria | Movimiento no autorizado |
| `MEDIUM` | Advertencia | Gas > 400 ppm |
| `LOW` | Informativo | NFC autenticado |

### Estados de Alerta

| Estado | Descripción |
|--------|-------------|
| `active` | Sin atender |
| `acknowledged` | Vista / reconocida por operador |
| `resolved` | Resuelta y documentada |

---

## 🧪 Tests

```bash
cd backend

# Todos los tests
uv run pytest

# Por tipo
uv run pytest -m unit          # Tests unitarios rápidos
uv run pytest -m integration   # Tests con base de datos
uv run pytest -m e2e           # Flujo completo

# Con reporte de cobertura
uv run pytest --cov=app --cov-report=html
```

---

## 🐳 Despliegue en Raspberry Pi 3B+

### Con Docker Compose

```bash
# En la RPi, clonar el repo
git clone https://github.com/LNieto-V/Ubicua-TODO.git
cd Ubicua-TODO/backend

# Construir y arrancar
docker compose up -d

# Ver logs
docker compose logs -f backend
```

El `docker-compose.yml` ya configura:
- Límite de 400 MB RAM (optimizado para RPi 3B+)
- Mapeo de `/dev` para acceso al puerto serial USB
- Volúmenes persistentes para `data/` y `cache/`

### Sin Docker (nativo)

```bash
# Instalar uv en la RPi
curl -LsSf https://astral.sh/uv/install.sh | sh

cd Ubicua-TODO/backend
uv sync

# Configurar variables de entorno
echo "ESP32_SERIAL_PORT=/dev/ttyUSB0" >> .env

# Arrancar como servicio
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 \
  --workers 1 --limit-concurrency 50
```

---

## 🛠️ Stack Tecnológico

### Backend
| Tecnología | Versión | Rol |
|-----------|---------|-----|
| FastAPI | 0.104+ | Framework web async |
| SQLAlchemy | 2.0+ | ORM async |
| aiosqlite | 0.19+ | Driver SQLite async |
| Pydantic v2 | 2.5+ | Validación / schemas |
| python-socketio | 5.x | WebSocket (Socket.IO) |
| serial-asyncio | 0.6+ | Comunicación serial async |
| diskcache | 5.6+ | Caché en disco |
| uvicorn | 0.24+ | Servidor ASGI |
| uv | 0.4+ | Gestión de entorno |

### Frontend
| Tecnología | Versión | Rol |
|-----------|---------|-----|
| React | 18 | UI framework |
| Vite | 5 | Build tool |
| TypeScript | 5 | Tipado estático |
| Tailwind CSS | 3 | Estilos utilitarios |
| React Query | 5 | Server state / caché |
| Zustand | 4 | Client state |
| Recharts | 2 | Gráficos de sensores |
| Axios | 1.6 | HTTP client |
| Socket.IO client | 4 | WebSocket |
| React Router | 6 | Navegación SPA |
| Lucide React | — | Iconografía |

---

## 👥 Equipo — Grupo 4

| Integrante | Rol |
|-----------|-----|
| Adriana María Bonilla Arias | Líder de proyecto / Backend |
| Eduar Ramos | Frontend / Hardware ESP32 |
| *(demás integrantes)* | Hardware / Testing |

---

## 📄 Licencia

Proyecto académico — Ingeniería en Sistemas · 2026  
Universidad de Cundinamarca
