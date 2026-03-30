"""
Chapter and Module models
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.progress import ChapterProgress, QuizAttempt, QuizQuestion


class Module(SQLModel, table=True):
    """Course module model"""
    __tablename__ = "modules"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(None)
    module_order: int = Field(..., unique=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships - using string back_populates
    chapters: List["Chapter"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
        back_populates="module"
    )


class Chapter(SQLModel, table=True):
    """Chapter model"""
    __tablename__ = "chapters"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    chapter_number: int = Field(..., index=True)
    module_id: int = Field(..., foreign_key="modules.id", index=True)
    title: str = Field(..., max_length=500)
    content: str = Field(...)  # Markdown content
    content_html: Optional[str] = Field(None)  # HTML rendered version
    is_free: bool = Field(default=False, index=True)
    estimated_minutes: int = Field(default=15)
    order_in_module: int = Field(...)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships - using string back_populates
    module: Optional[Module] = Relationship(back_populates="chapters")
    # Remove back_populates for now to avoid circular dependency
    # Will be configured after all models are imported
