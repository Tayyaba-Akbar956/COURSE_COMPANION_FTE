"""
Progress and Quiz models
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.chapter import Chapter


class ChapterProgress(SQLModel, table=True):
    """User chapter progress model"""
    __tablename__ = "chapter_progress"
    
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(..., foreign_key="users.id", index=True)
    chapter_id: int = Field(..., foreign_key="chapters.id", index=True)
    completed: bool = Field(default=False, index=True)
    completed_at: Optional[datetime] = Field(None)
    time_spent_seconds: int = Field(default=0)
    last_accessed_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships - no back_populates to avoid circular dependency
    user: Optional["User"] = Relationship()
    chapter: Optional["Chapter"] = Relationship()


class QuizQuestion(SQLModel, table=True):
    """Quiz question model"""
    __tablename__ = "quiz_questions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    chapter_id: int = Field(..., foreign_key="chapters.id", index=True)
    question_text: str = Field(...)
    options_json: str = Field(default="{}", sa_column_kwargs={"name": "options"})  # JSON string
    correct_answer: str = Field(..., max_length=10)
    explanation: Optional[str] = Field(None)
    why_wrong: Optional[str] = Field(None)
    source_reference: Optional[str] = Field(None, max_length=500)
    difficulty: str = Field(default="medium", max_length=20)
    order_in_chapter: int = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    chapter: Optional["Chapter"] = Relationship()


class QuizAttempt(SQLModel, table=True):
    """Quiz attempt model"""
    __tablename__ = "quiz_attempts"
    
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(..., foreign_key="users.id", index=True)
    chapter_id: int = Field(..., foreign_key="chapters.id", index=True)
    quiz_session_id: str = Field(..., unique=True, index=True)
    score: int = Field(..., ge=0, le=100)
    total_questions: int = Field(...)
    correct_answers: int = Field(...)
    incorrect_answers: int = Field(...)
    passed: bool = Field(...)
    passing_score: int = Field(default=80)
    answers_json: str = Field(default="{}", sa_column_kwargs={"name": "answers"})  # JSON string
    time_taken_seconds: Optional[int] = Field(None)
    attempt_number: int = Field(...)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional["User"] = Relationship()
    chapter: Optional["Chapter"] = Relationship()
