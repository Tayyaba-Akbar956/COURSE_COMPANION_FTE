"""
Simple smoke test to verify the API starts and responds
"""

import pytest
from httpx import AsyncClient


class TestSmokeTest:
    """Basic smoke tests"""
    
    @pytest.mark.anyio
    async def test_health_check(self, client: AsyncClient):
        """Should return health check response"""
        # Act
        response = await client.get("/health")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
    
    @pytest.mark.anyio
    async def test_root_endpoint(self, client: AsyncClient):
        """Should return API information"""
        # Act
        response = await client.get("/")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "docs" in data
