"""
Achievement and Streak models
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from uuid import uuid4

if TYPE_CHECKING:
    from app.models.user import User


class Achievement(SQLModel, table=True):
    """Achievement definition model"""
    __tablename__ = "achievements"
    
    id: str = Field(..., primary_key=True, max_length=100)
    name: str = Field(..., max_length=255)
    description: str = Field(...)
    icon: str = Field(..., max_length=50)
    criteria_json: str = Field(default="{}", sa_column_kwargs={"name": "criteria"})  # JSON string
    achievement_order: int = Field(..., unique=True)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    user_achievements: List["UserAchievement"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
        back_populates="achievement"
    )


class UserAchievement(SQLModel, table=True):
    """User achievement model"""
    __tablename__ = "user_achievements"
    
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(..., foreign_key="users.id", index=True)
    achievement_id: str = Field(..., foreign_key="achievements.id", index=True)
    unlocked_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional["User"] = Relationship()
    achievement: Optional[Achievement] = Relationship(back_populates="user_achievements")


class DailyStreak(SQLModel, table=True):
    """Daily activity streak model"""
    __tablename__ = "daily_streaks"
    
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(..., foreign_key="users.id", index=True)
    activity_date: datetime = Field(..., index=True)
    chapters_completed: int = Field(default=0)
    quizzes_taken: int = Field(default=0)
    minutes_spent: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationship
    user: Optional["User"] = Relationship()
