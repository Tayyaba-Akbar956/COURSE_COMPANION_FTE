"""
User and Subscription models
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from app.models.progress import ChapterProgress, QuizAttempt
    from app.models.achievement import UserAchievement, DailyStreak


class SubscriptionTier(str, Enum):
    """Subscription tier enum"""
    FREE = "free"
    PREMIUM = "premium"
    PRO = "pro"
    TEAM = "team"


class SubscriptionStatus(str, Enum):
    """Subscription status enum"""
    FREE = "free"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PAST_DUE = "past_due"


class User(SQLModel, table=True):
    """User model"""
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    email: str = Field(..., unique=True, index=True, max_length=255)
    full_name: Optional[str] = Field(None, max_length=255)
    avatar_url: Optional[str] = Field(None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Subscription(SQLModel, table=True):
    """User subscription model"""
    __tablename__ = "subscriptions"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(..., unique=True, foreign_key="users.id", index=True)
    tier: SubscriptionTier = Field(default=SubscriptionTier.FREE)
    status: SubscriptionStatus = Field(default=SubscriptionStatus.FREE)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = Field(None)
    auto_renew: bool = Field(default=False)
    stripe_subscription_id: Optional[str] = Field(None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship - no back_populates to avoid circular dependency
    user: Optional[User] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "Subscription.user_id"}
    )
