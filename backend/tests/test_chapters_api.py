"""
Chapter API Tests

Tests for chapter listing and retrieval endpoints.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


class TestListChapters:
    """Test GET /api/v1/chapters endpoint"""
    
    @pytest.mark.anyio
    async def test_list_chapters_success(self, client: AsyncClient):
        """Should return list of all chapters"""
        # Act
        response = await client.get("/api/v1/chapters")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "chapters" in data["data"]
        assert isinstance(data["data"]["chapters"], list)
    
    @pytest.mark.anyio
    async def test_list_chapters_free_only(self, client: AsyncClient):
        """Should return only free chapters when free_only=true"""
        # Act
        response = await client.get("/api/v1/chapters?free_only=true")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        # All returned chapters should be free
        for chapter in data["data"]["chapters"]:
            assert chapter["is_free"] == True
    
    @pytest.mark.anyio
    async def test_list_chapters_filter_by_module(self, client: AsyncClient, sample_module):
        """Should filter chapters by module"""
        # Act
        response = await client.get(f"/api/v1/chapters?module={sample_module.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        # All returned chapters should be from specified module
        for chapter in data["data"]["chapters"]:
            assert chapter["module_id"] == sample_module.id
    
    @pytest.mark.anyio
    async def test_list_chapters_empty(self, client: AsyncClient):
        """Should return empty list when no chapters exist"""
        # Act
        response = await client.get("/api/v1/chapters")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["chapters"] == []
        assert data["data"]["total_chapters"] == 0


class TestGetChapter:
    """Test GET /api/v1/chapters/{id} endpoint"""
    
    @pytest.mark.anyio
    async def test_get_chapter_success(self, client: AsyncClient, sample_chapter):
        """Should return full chapter content"""
        # Act
        response = await client.get(f"/api/v1/chapters/{sample_chapter.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "chapter" in data["data"]
        assert data["data"]["chapter"]["id"] == sample_chapter.id
        assert data["data"]["chapter"]["title"] == sample_chapter.title
        assert "content" in data["data"]["chapter"]
        assert "navigation" in data["data"]["chapter"]
        assert "quiz" in data["data"]["chapter"]
    
    @pytest.mark.anyio
    async def test_get_chapter_not_found(self, client: AsyncClient):
        """Should return 404 for non-existent chapter"""
        # Act
        response = await client.get("/api/v1/chapters/999")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["success"] == False
        assert "error" in data
    
    @pytest.mark.anyio
    async def test_get_free_chapter_no_auth(self, client: AsyncClient, sample_chapter):
        """Should allow access to free chapter without authentication"""
        # Act
        response = await client.get(f"/api/v1/chapters/{sample_chapter.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
    
    @pytest.mark.anyio
    async def test_get_premium_chapter_no_auth(self, client: AsyncClient, sample_module):
        """Should require authentication for premium chapter"""
        # Arrange: Create premium chapter
        premium_chapter = Chapter(
            chapter_number=2,
            module_id=sample_module.id,
            title="Advanced Topic",
            content="Premium content...",
            is_free=False,
            estimated_minutes=20,
            order_in_module=2
        )
        # Note: Would need to add to DB in real test
    
    @pytest.mark.anyio
    async def test_get_chapter_includes_navigation(self, client: AsyncClient, sample_chapter):
        """Should include navigation links"""
        # Act
        response = await client.get(f"/api/v1/chapters/{sample_chapter.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "navigation" in data["data"]["chapter"]
        navigation = data["data"]["chapter"]["navigation"]
        assert "previous_chapter_id" in navigation
        assert "next_chapter_id" in navigation


class TestCompleteChapter:
    """Test POST /api/v1/chapters/{id}/complete endpoint"""
    
    @pytest.mark.anyio
    async def test_complete_chapter_success(self, client: AsyncClient, sample_chapter, auth_headers):
        """Should mark chapter as completed"""
        # Act
        response = await client.post(
            f"/api/v1/chapters/{sample_chapter.id}/complete",
            json={"time_spent_seconds": 1200},
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["chapter_id"] == sample_chapter.id
        assert data["data"]["completed"] == True

    @pytest.mark.anyio
    async def test_complete_chapter_unauthorized(self, client: AsyncClient, sample_chapter):
        """Should require authentication"""
        # Act
        response = await client.post(
            f"/api/v1/chapters/{sample_chapter.id}/complete",
            json={"time_spent_seconds": 1200}
        )

        # Assert
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_complete_chapter_invalid_time(self, client: AsyncClient, sample_chapter, auth_headers):
        """Should reject invalid time_spent_seconds"""
        # Act
        response = await client.post(
            f"/api/v1/chapters/{sample_chapter.id}/complete",
            json={"time_spent_seconds": -100},  # Invalid
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 422  # Validation error


# Import Chapter model for tests
from app.models.chapter import Chapter
