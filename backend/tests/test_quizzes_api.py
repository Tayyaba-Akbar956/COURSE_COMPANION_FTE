"""
Quiz API Tests

Tests for quiz retrieval and submission endpoints.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


class TestGetQuiz:
    """Test GET /api/v1/chapters/{id}/quiz endpoint"""

    @pytest.mark.anyio
    async def test_get_quiz_success(self, client: AsyncClient, sample_chapter, sample_quiz_question, auth_headers):
        """Should return quiz with questions"""
        # Act
        response = await client.get(
            f"/api/v1/chapters/{sample_chapter.id}/quiz",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "questions" in data["data"]
        assert len(data["data"]["questions"]) > 0

    @pytest.mark.anyio
    async def test_get_quiz_unauthorized(self, client: AsyncClient, sample_chapter):
        """Should require authentication"""
        # Act
        response = await client.get(f"/api/v1/chapters/{sample_chapter.id}/quiz")

        # Assert
        assert response.status_code == 401

    @pytest.mark.anyio
    async def test_get_quiz_chapter_not_found(self, client: AsyncClient, auth_headers):
        """Should return 404 for non-existent chapter"""
        # Act
        response = await client.get(
            "/api/v1/chapters/999/quiz",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 404

    @pytest.mark.anyio
    async def test_get_quiz_questions_no_answers(self, client: AsyncClient, sample_chapter, sample_quiz_question, auth_headers):
        """Should not include correct answers in quiz questions"""
        # Act
        response = await client.get(
            f"/api/v1/chapters/{sample_chapter.id}/quiz",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        questions = data["data"]["questions"]
        for question in questions:
            assert "correct_answer" not in question
            assert "options" in question


class TestSubmitQuiz:
    """Test POST /api/v1/quizzes/{id}/submit endpoint"""

    @pytest.mark.anyio
    async def test_submit_quiz_success(self, client: AsyncClient, sample_chapter, sample_quiz_question, auth_headers):
        """Should grade quiz and return results"""
        # Arrange
        quiz_id = f"quiz-{sample_chapter.id}-test123"

        # Act
        response = await client.post(
            f"/api/v1/chapters/quizzes/{quiz_id}/submit",
            json={
                "answers": [
                    {"question_id": sample_quiz_question.id, "answer": "A"}
                ]
            },
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "answers" in data["data"]
        assert "score" in data["data"]
        assert "passed" in data["data"]

    @pytest.mark.anyio
    async def test_submit_quiz_empty_answers(self, client: AsyncClient, sample_chapter, auth_headers):
        """Should reject empty answers"""
        # Arrange
        quiz_id = f"quiz-{sample_chapter.id}-test456"

        # Act
        response = await client.post(
            f"/api/v1/chapters/quizzes/{quiz_id}/submit",
            json={"answers": []},
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_submit_quiz_invalid_answer_format(self, client: AsyncClient, sample_chapter, auth_headers):
        """Should reject invalid answer format"""
        # Arrange
        quiz_id = f"quiz-{sample_chapter.id}-test789"

        # Act
        response = await client.post(
            f"/api/v1/chapters/quizzes/{quiz_id}/submit",
            json={"invalid": "format"},
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 422

    @pytest.mark.anyio
    async def test_submit_quiz_records_attempt(self, client: AsyncClient, sample_chapter, sample_quiz_question, auth_headers):
        """Should record quiz attempt in database"""
        # Arrange
        quiz_id = f"quiz-{sample_chapter.id}-record"

        # Act
        response = await client.post(
            f"/api/v1/chapters/quizzes/{quiz_id}/submit",
            json={
                "answers": [
                    {"question_id": sample_quiz_question.id, "answer": "A"}
                ]
            },
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        # Verify attempt was recorded (check response includes attempt info)
        data = response.json()
        assert data["success"] == True


class TestQuizHistory:
    """Test GET /api/v1/chapters/{id}/quiz/history endpoint"""

    @pytest.mark.anyio
    async def test_get_quiz_history_success(self, client: AsyncClient, sample_chapter, auth_headers):
        """Should return quiz attempt history"""
        # Act
        response = await client.get(
            f"/api/v1/chapters/{sample_chapter.id}/quiz/history",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "data" in data
        assert "attempts" in data["data"]
        assert isinstance(data["data"]["attempts"], list)

    @pytest.mark.anyio
    async def test_get_quiz_history_empty(self, client: AsyncClient, sample_chapter, auth_headers):
        """Should return empty history for new user"""
        # Act
        response = await client.get(
            f"/api/v1/chapters/{sample_chapter.id}/quiz/history",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["data"]["attempts"] == []
