import socketio
from fastapi import APIRouter

# Creamos el servidor Socket.IO asíncrono
# Se permite CORS para que el frontend pueda conectarse
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
sio_app = socketio.ASGIApp(sio)

router = APIRouter(prefix="/ws", tags=["Websocket"])

@sio.event
async def connect(sid, environ):
    print(f"Cliente conectado: {sid}")
    await sio.emit('system_status', {'data': 'Conectado al servidor de alertas'}, to=sid)

@sio.event
async def disconnect(sid):
    print(f"Cliente desconectado: {sid}")

@sio.event
async def subscribe(sid, data):
    """
    Permite al cliente suscribirse a canales específicos (ej: 'alerts' o 'readings').
    """
    room = data.get('channel')
    if room:
        sio.enter_room(sid, room)
        await sio.emit('notification', {'msg': f'Suscrito a {room}'}, to=sid)

# Función utilitaria para emitir alertas desde cualquier parte del backend
async def broadcast_alert(alert_data: dict):
    await sio.emit('alert_triggered', alert_data, room='alerts')

async def broadcast_reading(reading_data: dict):
    await sio.emit('new_reading', reading_data, room='readings')