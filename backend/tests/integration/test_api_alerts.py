import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.integration
async def test_get_alerts_empty_list():
    """Verifica que el endpoint de alertas responda correctamente."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/alerts/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)