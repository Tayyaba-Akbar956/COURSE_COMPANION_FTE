# SPEC-A-003-progress-apis-v1.0

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

This spec defines the API contract for progress tracking endpoints including chapter progress, quiz history, streaks, achievements, and overall course progress.

## 2. API Endpoints

### 2.1 GET /api/v1/users/{user_id}/progress

**Description:** Get comprehensive progress for a user

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "user_id": "user123",
    "overall_progress": {
      "chapters_completed": 5,
      "total_chapters": 24,
      "completion_percentage": 20.8,
      "quizzes_completed": 4,
      "average_quiz_score": 87.5,
      "time_spent_minutes": 320
    },
    "streak": {
      "current_streak": 5,
      "longest_streak": 7,
      "streak_active": true
    },
    "module_progress": [
      {
        "module_id": 1,
        "module_title": "Introduction to Generative AI",
        "chapters_completed": 3,
        "total_chapters": 4,
        "completion_percentage": 75
      }
    ],
    "achievements": {
      "earned": [
        {"achievement_id": "first_chapter", "name": "First Steps", "icon": "🏅", "unlocked_at": "..."}
      ],
      "locked": [
        {"achievement_id": "streak_10", "name": "Dedicated Scholar", "icon": "⚡", "progress": 5, "target": 10}
      ]
    }
  }
}
```

**Errors:** 401 (Unauthorized), 403 (Can only access own progress)

---

### 2.2 PUT /api/v1/users/{user_id}/progress

**Description:** Update user progress (after chapter completion)

**Request Body:**
```json
{
  "chapter_id": 7,
  "action": "complete",
  "time_spent_seconds": 1200
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "chapter_id": 7,
    "completed": true,
    "achievements_unlocked": [
      {"achievement_id": "module_2_complete", "name": "Module 2 Master", "icon": "🎯"}
    ],
    "streak_updated": {"current_streak": 5, "streak_maintained": true},
    "new_completion_percentage": 25.0
  }
}
```

**Errors:** 401 (Unauthorized), 400 (Invalid Action)

---

### 2.3 POST /api/v1/users/{user_id}/progress/quiz

**Description:** Record quiz completion

**Request Body:**
```json
{
  "chapter_id": 7,
  "quiz_id": "quiz-session-xyz",
  "score": 80,
  "passed": true,
  "time_taken_seconds": 180
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "quiz_recorded": {"chapter_id": 7, "score": 80, "passed": true},
    "new_average_score": 86.4
  }
}
```

---

### 2.4 GET /api/v1/users/{user_id}/progress/export

**Description:** Export all progress data (GDPR compliance)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "export_generated_at": "2026-03-29T12:00:00Z",
    "download_url": "https://r2.example.com/exports/user123-progress.json",
    "expires_at": "2026-04-05T12:00:00Z"
  }
}
```

---

### 2.5 GET /api/v1/users/{user_id}/streak

**Description:** Get current streak information

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "current_streak": 5,
    "longest_streak": 7,
    "streak_start_date": "2026-03-25",
    "last_activity_date": "2026-03-29",
    "streak_active": true
  }
}
```

---

### 2.6 GET /api/v1/users/{user_id}/achievements

**Description:** Get all achievements (earned and locked)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "earned": [...],
    "locked": [...],
    "total_earned": 3,
    "total_available": 6
  }
}
```

---

## 3. Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| GET /users/{id}/progress | 60 | per minute |
| PUT /users/{id}/progress | 30 | per minute |
| GET /users/{id}/progress/export | 5 | per hour |

## 4. Testing Requirements

```python
def test_progress_api_get_progress():
    """Should return comprehensive progress"""
    # Act: GET /api/v1/users/{id}/progress
    # Assert: 200 OK, chapters_completed, streak, achievements

def test_progress_api_update_chapter():
    """Should mark chapter as completed"""
    # Act: PUT /api/v1/users/{id}/progress
    # Assert: 200 OK, completed=true, achievements checked

def test_progress_api_record_quiz():
    """Should record quiz score"""
    # Act: POST /api/v1/users/{id}/progress/quiz
    # Assert: 200 OK, score recorded, average updated

def test_progress_api_streak_calculation():
    """Should calculate streak correctly"""
    # Act: 5 consecutive days of activity
    # Assert: current_streak=5

def test_progress_api_export():
    """Should generate export file"""
    # Act: GET /api/v1/users/{id}/progress/export
    # Assert: 200 OK, download_url provided
```

## 5. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Progress APIs Spec (SPEC-A-003-progress-apis-v1.0)  
**Why:** Defines progress tracking endpoints for student journey monitoring  
**Files Affected:** `docs/specs/api/SPEC-A-003-progress-apis-v1.0.md`

**Key Decisions:**
- Comprehensive progress in single endpoint
- Real-time streak calculation
- Achievement auto-unlocking
- GDPR-compliant export
- Progress updates trigger achievement checks

**Do you approve?** (Yes/No/Modify)

---

**Progress:** API Specs: 3/5 Complete. Remaining: A-004 (Auth), A-005 (Search)
