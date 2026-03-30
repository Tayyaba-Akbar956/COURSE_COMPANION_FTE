# SPEC-A-001-content-apis-v1.0

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

This spec defines the complete API contract for content-related endpoints including listing chapters, retrieving chapter content, searching content, and accessing course structure.

## 2. API Design Principles

- **RESTful:** Resources as nouns, HTTP methods for operations
- **Versioned:** `/api/v1/` prefix
- **JSON Responses:** Consistent structure
- **Authenticated:** JWT required for all endpoints

## 3. API Endpoints

### 3.1 GET /api/v1/chapters

**Description:** List all chapters with metadata

**Query Parameters:** `module` (int), `include_progress` (bool), `free_only` (bool)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "chapters": [
      {
        "id": 1,
        "chapter_number": 1,
        "module_id": 1,
        "title": "What is Generative AI?",
        "is_free": true,
        "estimated_minutes": 15,
        "user_progress": {"completed": true, "quiz_score": 100}
      }
    ],
    "total_chapters": 24
  }
}
```

**Errors:** 401 (Unauthorized), 403 (Access Denied)

---

### 3.2 GET /api/v1/chapters/{chapter_id}

**Description:** Get full chapter content

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "chapter": {
      "id": 1,
      "title": "What is Generative AI?",
      "content": "# What is Generative AI?\\n\\n...",
      "sections": [{"id": "section-1", "title": "Introduction", "content": "..."}],
      "images": [{"url": "https://cdn.example.com/...", "alt": "...", "caption": "..."}],
      "code_examples": [{"language": "python", "code": "...", "description": "..."}],
      "navigation": {"previous_chapter_id": null, "next_chapter_id": 2}
    }
  }
}
```

**Errors:** 401 (Unauthorized), 403 (Access Denied), 404 (Not Found)

---

### 3.3 GET /api/v1/search

**Description:** Search across all chapter content

**Query Parameters:** `q` (required, string), `limit` (int, default 10), `offset` (int, default 0)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "query": "transformer",
    "results": [
      {
        "type": "chapter_section",
        "chapter_id": 6,
        "chapter_title": "How LLMs Work",
        "section_title": "Self-Attention",
        "excerpt": "The transformer architecture uses...",
        "relevance_score": 0.95,
        "is_free": false
      }
    ],
    "total_results": 15
  }
}
```

**Errors:** 400 (Missing Query), 401 (Unauthorized)

---

### 3.4 GET /api/v1/course/structure

**Description:** Return complete course structure (modules and chapters)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "course": {"title": "Generative AI Fundamentals", "total_chapters": 24, "total_modules": 6},
    "modules": [
      {
        "id": 1,
        "title": "Introduction to Generative AI",
        "module_order": 1,
        "chapters": [{"id": 1, "title": "What is Generative AI?", "is_free": true}]
      }
    ]
  }
}
```

---

### 3.5 POST /api/v1/chapters/{chapter_id}/complete

**Description:** Mark chapter as completed

**Request Body:** `{"time_spent_seconds": 900}`

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "chapter_id": 1,
    "completed": true,
    "completed_at": "2026-03-29T12:30:00Z",
    "achievements_unlocked": [{"achievement_id": "first_chapter", "name": "First Steps"}]
  }
}
```

**Errors:** 401 (Unauthorized), 403 (Access Denied), 404 (Not Found)

---

### 3.6 GET /api/v1/chapters/{chapter_id}/markdown

**Description:** Return chapter content in markdown format (for ChatGPT app)

**Response:** `Content-Type: text/markdown`

---

## 4. Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| GET /chapters | 100 | per minute |
| GET /chapters/{id} | 200 | per minute |
| GET /search | 60 | per minute |

**429 Response:** `{"error": {"code": "RATE_LIMIT_EXCEEDED", "message": "Too many requests"}}`

## 5. Testing Requirements

```python
def test_content_api_list_chapters():
    """Should return list of all chapters"""
    # Act: GET /api/v1/chapters
    # Assert: 200 OK, chapters array

def test_content_api_get_chapter():
    """Should return chapter content"""
    # Act: GET /api/v1/chapters/1
    # Assert: 200 OK, content with sections, images, code

def test_content_api_get_chapter_premium_only():
    """Should deny access to premium chapter for free user"""
    # Act: GET /api/v1/chapters/5 (free user)
    # Assert: 403 Forbidden

def test_content_api_search():
    """Should return relevant search results"""
    # Act: GET /api/v1/search?q=transformer
    # Assert: 200 OK, results with relevance scores

def test_content_api_mark_complete():
    """Should mark chapter as completed"""
    # Act: POST /api/v1/chapters/1/complete
    # Assert: 200 OK, completed=true

def test_content_api_rate_limiting():
    """Should rate limit excessive requests"""
    # Act: 101 requests in 1 minute
    # Assert: 429 on 101st request
```

## 6. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Content APIs Spec (SPEC-A-001-content-apis-v1.0)  
**Why:** Defines all content-related API endpoints for frontend integration  
**Files Affected:** `docs/specs/api/SPEC-A-001-content-apis-v1.0.md`

**Key Decisions:**
- RESTful API with JSON responses
- Versioned URLs (`/api/v1/`)
- Rate limiting on all endpoints
- Markdown format for ChatGPT app
- Search with relevance scoring

**Do you approve this spec?** (Yes/No/Modify)

---

**Progress:** API Specs: 1/5 Complete. Remaining: A-002 (Quiz), A-003 (Progress), A-004 (Auth), A-005 (Search)
