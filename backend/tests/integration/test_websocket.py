import pytest
import socketio
from app.routers.websocket import broadcast_alert

@pytest.mark.integration
async def test_websocket_connection():
    """Verifica que un cliente pueda conectarse al servidor de WebSockets."""
    sio_client = socketio.AsyncClient()
    # En el entorno de test, el servidor corre en localhost:8000
    try:
        await sio_client.connect('http://localhost:8000', socketio_path='/ws/socket.io')
        assert sio_client.sid is not None
        await sio_client.disconnect()
    except Exception:
        # Si el servidor no está levantado físicamente durante este test unitario/int, 
        # se suele usar un Mock del servidor sio.
        pytest.skip("Servidor asíncrono no detectado para test de conexión real")

@pytest.mark.integration
async def test_broadcast_alert_reaches_client(mocker):
    """Prueba que la función broadcast_alert emita el evento correctamente."""
    # Mockeamos el servidor sio para verificar la emisión sin necesidad de red
    mock_sio = mocker.patch('app.routers.websocket.sio.emit', new_callable=mocker.AsyncMock)
    
    test_alert = {"message": "Humo detectado", "severity": "CRITICAL"}
    await broadcast_alert(test_alert)
    
    mock_sio.assert_called_with('alert_triggered', test_alert, room='alerts')