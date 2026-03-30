# SPEC-S-001-pydantic-schemas-v1.0

## Status
- [x] Draft
- [ ] Pending Approval
- [ ] Approved
- [ ] In Progress
- [ ] Completed
- [ ] Deprecated

## Metadata
- **Created:** 2026-03-29
- **Author:** Qwen Code (AI Builder)
- **Approved By:** [Pending User Approval]
- **Version:** 1.0.0

## 1. Overview

This spec defines all Pydantic schemas for request/response validation across the API. These schemas ensure type safety, validation, and consistent API contracts.

## 2. Chapter Schemas

### 2.1 Chapter Response

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ChapterSection(BaseModel):
    """Chapter section model"""
    id: str
    title: str
    content: str
    order: int
    word_count: Optional[int] = None

class ChapterImage(BaseModel):
    """Chapter image model"""
    id: str
    url: str = Field(..., description="CDN URL")
    alt: str
    caption: str
    section_id: Optional[str] = None

class CodeExample(BaseModel):
    """Code example model"""
    id: str
    language: str = Field(..., example="python")
    code: str
    description: str
    section_id: Optional[str] = None

class ChapterNavigation(BaseModel):
    """Navigation links model"""
    previous_chapter_id: Optional[int] = None
    next_chapter_id: Optional[int] = None
    previous_chapter_title: Optional[str] = None
    next_chapter_title: Optional[str] = None

class ChapterQuizInfo(BaseModel):
    """Quiz availability info"""
    available: bool
    quiz_id: Optional[int] = None
    total_questions: Optional[int] = None
    passing_score: Optional[int] = 80

class ChapterResponse(BaseModel):
    """Full chapter response"""
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

    class Config:
        from_attributes = True
```

### 2.2 Chapter List Response

```python
class ChapterListItem(BaseModel):
    """Chapter list item (summary)"""
    id: int
    chapter_number: int
    module_id: int
    module_title: str
    title: str
    is_free: bool
    estimated_minutes: int
    order_in_module: int
    quiz_available: bool

class ChapterListResponse(BaseModel):
    """Chapter list response"""
    success: bool
    data: dict
    meta: dict

class ChapterListData(BaseModel):
    """Chapter list data"""
    chapters: List[ChapterListItem]
    total_chapters: int
    returned_chapters: int
    filters_applied: dict

class MetaInfo(BaseModel):
    """Response metadata"""
    request_id: str
    timestamp: datetime
    execution_time_ms: int
```

### 2.3 Chapter Completion Request

```python
class ChapterCompleteRequest(BaseModel):
    """Request to mark chapter as complete"""
    time_spent_seconds: Optional[int] = Field(None, ge=0, le=86400)

class ChapterCompleteResponse(BaseModel):
    """Chapter completion response"""
    success: bool
    data: dict

class ChapterCompleteData(BaseModel):
    """Completion data"""
    chapter_id: int
    completed: bool
    completed_at: datetime
    time_spent_seconds: Optional[int]
    achievements_unlocked: List[dict]
```

## 3. Quiz Schemas

### 3.1 Quiz Question

```python
class QuizOption(BaseModel):
    """Quiz option model"""
    id: str = Field(..., pattern="^[A-D]$")
    text: str

class QuizQuestion(BaseModel):
    """Quiz question model"""
    question_id: int
    question_text: str
    options: List[QuizOption]
    question_number: int

class QuizResponse(BaseModel):
    """Quiz response"""
    success: bool
    data: dict

class QuizData(BaseModel):
    """Quiz data"""
    quiz_id: str
    chapter_id: int
    chapter_title: str
    total_questions: int
    passing_score: int = 80
    questions: List[QuizQuestion]
```

### 3.2 Quiz Submission

```python
class QuizAnswer(BaseModel):
    """Single quiz answer"""
    question_id: int
    answer: str = Field(..., pattern="^[A-D]$")

class QuizSubmitRequest(BaseModel):
    """Quiz submission request"""
    answers: List[QuizAnswer]

    @validator('answers')
    def validate_answers(cls, v):
        if len(v) == 0:
            raise ValueError("At least one answer required")
        return v

class GradedAnswer(BaseModel):
    """Graded answer with feedback"""
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
    feedback: dict
    next_steps: dict

class QuizSubmitResponse(BaseModel):
    """Quiz submission response"""
    success: bool
    data: QuizResult
```

### 3.3 Quiz History

```python
class QuizAttemptSummary(BaseModel):
    """Quiz attempt summary"""
    quiz_id: str
    score: int
    passed: bool
    attempt_number: int
    submitted_at: datetime
    time_taken_seconds: Optional[int]

class QuizHistoryResponse(BaseModel):
    """Quiz history response"""
    success: bool
    data: dict

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
```

## 4. Progress Schemas

### 4.1 Progress Response

```python
class OverallProgress(BaseModel):
    """Overall course progress"""
    chapters_completed: int
    total_chapters: int
    completion_percentage: float = Field(..., ge=0, le=100)
    quizzes_completed: int
    total_quizzes: int
    average_quiz_score: Optional[float]
    time_spent_minutes: int
    first_activity: Optional[datetime]
    last_activity: Optional[datetime]

class StreakInfo(BaseModel):
    """Streak information"""
    current_streak: int
    longest_streak: int
    streak_start_date: Optional[datetime]
    last_activity_date: Optional[datetime]
    streak_active: bool

class ModuleProgress(BaseModel):
    """Module-level progress"""
    module_id: int
    module_title: str
    chapters_completed: int
    total_chapters: int
    completion_percentage: float
    quizzes_passed: int
    average_quiz_score: Optional[float]

class AchievementInfo(BaseModel):
    """Achievement information"""
    achievement_id: str
    name: str
    description: str
    icon: str
    unlocked_at: Optional[datetime] = None

class ProgressResponse(BaseModel):
    """Full progress response"""
    success: bool
    data: dict

class ProgressData(BaseModel):
    """Progress data"""
    user_id: str
    overall_progress: OverallProgress
    streak: StreakInfo
    module_progress: List[ModuleProgress]
    achievements: dict  # {earned: [], locked: []}
```

### 4.2 Progress Update

```python
class ProgressUpdateRequest(BaseModel):
    """Progress update request"""
    chapter_id: int
    action: str = Field(..., pattern="^(complete|in_progress|start)$")
    time_spent_seconds: Optional[int] = Field(None, ge=0)
    quiz_score: Optional[int] = Field(None, ge=0, le=100)

class ProgressUpdateResponse(BaseModel):
    """Progress update response"""
    success: bool
    data: dict

class ProgressUpdateData(BaseModel):
    """Progress update data"""
    chapter_id: int
    completed: bool
    achievements_unlocked: List[AchievementInfo]
    streak_updated: dict
    new_overall_progress: OverallProgress
```

## 5. Auth Schemas

### 5.1 Auth Request/Response

```python
class SignupRequest(BaseModel):
    """Signup request"""
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    auth_method: str = Field(default="magic_link", pattern="^(magic_link|oauth|password)$")
    password: Optional[str] = Field(None, min_length=8)

class LoginRequest(BaseModel):
    """Login request"""
    email: str
    auth_method: str = "magic_link"

class AuthResponse(BaseModel):
    """Auth response"""
    success: bool
    message: str
    email: str

class TokenRefreshRequest(BaseModel):
    """Token refresh request"""
    refresh_token: str

class TokenRefreshResponse(BaseModel):
    """Token refresh response"""
    access_token: str
    expires_in: int
    token_type: str = "Bearer"

class UserInfo(BaseModel):
    """User information"""
    user_id: str
    email: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    subscription_tier: str
    created_at: datetime

class UserInfoResponse(BaseModel):
    """User info response"""
    success: bool
    data: UserInfo
```

## 6. Search Schemas

### 6.1 Search Request/Response

```python
class SearchRequest(BaseModel):
    """Search request (query params)"""
    q: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=50)
    offset: int = Field(default=0, ge=0)
    module: Optional[int] = None
    free_only: bool = False

class SearchResult(BaseModel):
    """Search result item"""
    type: str = "chapter_section"
    chapter_id: int
    chapter_title: str
    section_id: Optional[str]
    section_title: Optional[str]
    content: str
    excerpt: str
    relevance_score: float = Field(..., ge=0, le=1)
    is_free: bool
    matched_terms: List[str]
    url: str

class SearchResponse(BaseModel):
    """Search response"""
    success: bool
    data: dict

class SearchData(BaseModel):
    """Search data"""
    query: str
    results: List[SearchResult]
    total_results: int
    returned_results: int
    limit: int
    offset: int
    filters_applied: dict
    search_metadata: dict
```

## 7. Error Schemas

### 7.1 Error Response

```python
class ErrorDetail(BaseModel):
    """Error detail model"""
    code: str
    message: str
    details: Optional[dict] = None

class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: ErrorDetail
    meta: MetaInfo

# Error codes
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
```

## 8. Implementation

### 8.1 File Structure

```
backend/app/schemas/
├── __init__.py
├── chapter.py          # Chapter schemas
├── quiz.py             # Quiz schemas
├── progress.py         # Progress schemas
├── auth.py             # Auth schemas
├── search.py           # Search schemas
├── error.py            # Error schemas
└── common.py           # Common schemas (MetaInfo, etc.)
```

### 8.2 Usage Example

```python
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chapter import ChapterResponse, ChapterListResponse
from app.schemas.error import ErrorResponse, ERROR_CODES

router = APIRouter()

@router.get("/chapters/{chapter_id}", response_model=ChapterResponse)
async def get_chapter(chapter_id: int):
    chapter = await get_chapter_from_db(chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=ERROR_CODES["CHAPTER_NOT_FOUND"]["status"],
            detail=ERROR_CODES["CHAPTER_NOT_FOUND"]["message"]
        )
    return chapter
```

## 9. Testing Requirements

```python
def test_schemas_chapter_response():
    """Chapter response schema should validate"""
    data = {"id": 1, "title": "...", ...}
    schema = ChapterResponse(**data)
    assert schema.id == 1

def test_schemas_quiz_submit_valid():
    """Valid quiz submission should validate"""
    data = {"answers": [{"question_id": 1, "answer": "A"}]}
    schema = QuizSubmitRequest(**data)
    assert len(schema.answers) == 1

def test_schemas_quiz_submit_invalid():
    """Invalid quiz submission should raise"""
    data = {"answers": []}
    with pytest.raises(ValidationError):
        QuizSubmitRequest(**data)

def test_schemas_error_response():
    """Error response schema should validate"""
    data = {"success": False, "error": {"code": "NOT_FOUND", "message": "..."}}
    schema = ErrorResponse(**data)
    assert schema.success == False
```

## 10. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Pydantic Schemas Spec (SPEC-S-001-pydantic-schemas-v1.0)  
**Why:** Defines all request/response models for type-safe API validation  
**Files Affected:** `docs/specs/technical/SPEC-S-001-pydantic-schemas-v1.0.md`

**Do you approve?** (Yes/No/Modify)

---

**Gap 1 Fixed!** ✅ Now creating remaining critical specs...
