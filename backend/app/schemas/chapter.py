"""
Pydantic Schemas for API validation

All request/response models for type-safe API.
"""

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict
from datetime import datetime
from typing import Optional, List, Any, Dict
from enum import Enum
import re


# =============================================================================
# Common Schemas
# =============================================================================

class MetaInfo(BaseModel):
    """Response metadata"""
    request_id: str
    timestamp: datetime
    execution_time_ms: int


class ErrorDetail(BaseModel):
    """Error detail"""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: ErrorDetail
    meta: MetaInfo


# =============================================================================
# Chapter Schemas
# =============================================================================

class ChapterSection(BaseModel):
    """Chapter section"""
    id: str
    title: str
    content: str
    order: int
    word_count: Optional[int] = None


class ChapterImage(BaseModel):
    """Chapter image"""
    id: str
    url: str = Field(..., description="CDN URL")
    alt: str
    caption: str
    section_id: Optional[str] = None


class CodeExample(BaseModel):
    """Code example"""
    id: str
    language: str
    code: str
    description: str
    section_id: Optional[str] = None


class ChapterNavigation(BaseModel):
    """Chapter navigation"""
    previous_chapter_id: Optional[int] = None
    next_chapter_id: Optional[int] = None
    previous_chapter_title: Optional[str] = None
    next_chapter_title: Optional[str] = None


class ChapterQuizInfo(BaseModel):
    """Chapter quiz info"""
    available: bool
    quiz_id: Optional[int] = None
    total_questions: Optional[int] = None
    passing_score: int = 80


class Chapter(BaseModel):
    """Full chapter response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    chapter_number: int
    module_id: int
    module_title: str
    title: str
    content: str
    content_html: Optional[str] = None
    is_free: bool
    estimated_minutes: int
    order_in_module: int
    sections: List[ChapterSection]
    images: List[ChapterImage]
    code_examples: List[CodeExample]
    navigation: ChapterNavigation
    quiz: ChapterQuizInfo
    created_at: datetime
    updated_at: datetime


class ChapterListItem(BaseModel):
    """Chapter list item"""
    id: int
    chapter_number: int
    module_id: int
    module_title: str
    title: str
    is_free: bool
    estimated_minutes: int
    order_in_module: int
    quiz_available: bool


class ChapterListData(BaseModel):
    """Chapter list data"""
    chapters: List[ChapterListItem]
    total_chapters: int
    returned_chapters: int
    filters_applied: Dict[str, Any]


class ChapterListResponse(BaseModel):
    """Chapter list response"""
    success: bool
    data: ChapterListData
    meta: MetaInfo


class ChapterCompleteRequest(BaseModel):
    """Mark chapter complete request"""
    time_spent_seconds: Optional[int] = Field(None, ge=0, le=86400)


class ChapterCompleteData(BaseModel):
    """Chapter completion data"""
    chapter_id: int
    completed: bool
    completed_at: datetime
    time_spent_seconds: Optional[int]
    achievements_unlocked: List[Dict[str, str]]


class ChapterCompleteResponse(BaseModel):
    """Chapter completion response"""
    success: bool
    data: ChapterCompleteData


# =============================================================================
# Quiz Schemas
# =============================================================================

class QuizOption(BaseModel):
    """Quiz option"""
    id: str = Field(..., pattern="^[A-D]$")
    text: str


class QuizQuestion(BaseModel):
    """Quiz question"""
    question_id: int
    question_text: str
    options: List[QuizOption]
    question_number: int


class QuizData(BaseModel):
    """Quiz data"""
    quiz_id: str
    chapter_id: int
    chapter_title: str
    total_questions: int
    passing_score: int = 80
    questions: List[QuizQuestion]


class QuizResponse(BaseModel):
    """Quiz response"""
    success: bool
    data: QuizData


class QuizAnswer(BaseModel):
    """Quiz answer"""
    question_id: int
    answer: str = Field(..., pattern="^[A-D]$")


class QuizSubmitRequest(BaseModel):
    """Quiz submission request"""
    answers: List[QuizAnswer]

    @field_validator('answers')
    @classmethod
    def validate_answers(cls, v):
        if len(v) == 0:
            raise ValueError("At least one answer required")
        return v


class GradedAnswer(BaseModel):
    """Graded answer"""
    question_id: int
    question_text: str
    student_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str
    why_wrong: Optional[str] = None
    source_reference: str


class QuizResult(BaseModel):
    """Quiz result"""
    quiz_id: str
    chapter_id: int
    user_id: str
    score: int = Field(..., ge=0, le=100)
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    passed: bool
    passing_score: int
    submitted_at: datetime
    time_taken_seconds: Optional[int]
    attempt_number: int
    answers: List[GradedAnswer]
    feedback: Dict[str, str]
    next_steps: Dict[str, Any]


class QuizSubmitResponse(BaseModel):
    """Quiz submission response"""
    success: bool
    data: QuizResult


class QuizAttemptSummary(BaseModel):
    """Quiz attempt summary"""
    quiz_id: str
    score: int
    passed: bool
    attempt_number: int
    submitted_at: datetime
    time_taken_seconds: Optional[int]


class QuizHistoryData(BaseModel):
    """Quiz history data"""
    chapter_id: int
    chapter_title: str
    total_attempts: int
    best_score: int
    latest_score: int
    average_score: float
    passed: bool
    attempts: List[QuizAttemptSummary]


class QuizHistoryResponse(BaseModel):
    """Quiz history response"""
    success: bool
    data: QuizHistoryData


# =============================================================================
# Progress Schemas
# =============================================================================

class OverallProgress(BaseModel):
    """Overall course progress"""
    chapters_completed: int
    total_chapters: int
    completion_percentage: float = Field(..., ge=0, le=100)
    quizzes_completed: int
    average_quiz_score: Optional[float]
    time_spent_minutes: int


class StreakInfo(BaseModel):
    """Streak information"""
    current_streak: int
    longest_streak: int
    streak_active: bool


class ModuleProgress(BaseModel):
    """Module progress"""
    module_id: int
    module_title: str
    chapters_completed: int
    total_chapters: int
    completion_percentage: float


class AchievementInfo(BaseModel):
    """Achievement info"""
    achievement_id: str
    name: str
    description: str
    icon: str
    unlocked_at: Optional[datetime] = None


class ProgressData(BaseModel):
    """Progress data"""
    user_id: str
    overall_progress: OverallProgress
    streak: StreakInfo
    module_progress: List[ModuleProgress]
    achievements: Dict[str, List[AchievementInfo]]


class ProgressResponse(BaseModel):
    """Progress response"""
    success: bool
    data: ProgressData


class ProgressUpdateRequest(BaseModel):
    """Progress update request"""
    chapter_id: int
    action: str = Field(..., pattern="^(complete|in_progress|start)$")
    time_spent_seconds: Optional[int] = Field(None, ge=0)


class ProgressUpdateData(BaseModel):
    """Progress update data"""
    chapter_id: int
    completed: bool
    achievements_unlocked: List[AchievementInfo]
    streak_updated: Dict[str, Any]
    new_overall_progress: OverallProgress


class ProgressUpdateResponse(BaseModel):
    """Progress update response"""
    success: bool
    data: ProgressUpdateData


# =============================================================================
# Auth Schemas
# =============================================================================

class SignupRequest(BaseModel):
    """Signup request"""
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    auth_method: str = Field(default="magic_link", pattern="^(magic_link|oauth|password)$")
    password: Optional[str] = Field(None, min_length=8)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v


class LoginRequest(BaseModel):
    """Login request"""
    email: str
    auth_method: str = "magic_link"


class AuthResponse(BaseModel):
    """Auth response"""
    success: bool
    message: str
    email: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class TokenRefreshRequest(BaseModel):
    """Token refresh request"""
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    """Token refresh response"""
    access_token: str
    expires_in: int
    token_type: str = "Bearer"


class UserInfo(BaseModel):
    """User info"""
    user_id: str
    email: str
    full_name: Optional[str] = None
    subscription_tier: str
    created_at: datetime


class UserInfoResponse(BaseModel):
    """User info response"""
    success: bool
    data: UserInfo


# =============================================================================
# Search Schemas
# =============================================================================

class SearchRequest(BaseModel):
    """Search request"""
    q: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=50)
    offset: int = Field(default=0, ge=0)
    module: Optional[int] = None
    free_only: bool = False


class SearchResult(BaseModel):
    """Search result"""
    type: str = "chapter_section"
    chapter_id: int
    chapter_title: str
    section_id: Optional[str]
    section_title: Optional[str]
    excerpt: str
    relevance_score: float = Field(..., ge=0, le=1)
    is_free: bool
    matched_terms: List[str]
    url: str


class SearchData(BaseModel):
    """Search data"""
    query: str
    results: List[SearchResult]
    total_results: int
    returned_results: int
    limit: int
    offset: int
    filters_applied: Dict[str, Any]
    search_metadata: Dict[str, Any]


class SearchResponse(BaseModel):
    """Search response"""
    success: bool
    data: SearchData
    meta: MetaInfo


# =============================================================================
# Error Codes
# =============================================================================

ERROR_CODES = {
    "UNAUTHORIZED": {"status": 401, "message": "Authentication required"},
    "INVALID_TOKEN": {"status": 401, "message": "Invalid or expired token"},
    "ACCESS_DENIED": {"status": 403, "message": "Access denied"},
    "CHAPTER_NOT_FOUND": {"status": 404, "message": "Chapter not found"},
    "QUIZ_NOT_FOUND": {"status": 404, "message": "Quiz not found"},
    "INVALID_REQUEST": {"status": 400, "message": "Invalid request"},
    "RATE_LIMIT_EXCEEDED": {"status": 429, "message": "Too many requests"},
    "INTERNAL_ERROR": {"status": 500, "message": "Internal server error"},
}
