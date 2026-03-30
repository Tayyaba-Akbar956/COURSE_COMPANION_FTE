# SPEC-F-001-content-delivery-v1.0

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

This spec defines the Content Delivery feature that serves course chapters verbatim from the database to students. The backend serves content exactly as stored, while ChatGPT handles explanations and adaptations.

## 2. Functional Requirements

### FR-1: Chapter Access
- Students can access individual chapters by ID
- Free users can access Chapters 1-4 (Module 1)
- Premium users can access all 24 chapters
- Content is served verbatim (no modifications)

### FR-2: Content Display
- Chapter content includes title, body, code examples, and images
- Content is formatted for readability (markdown rendering)
- Chapter metadata shows: chapter number, title, module, estimated time

### FR-3: Content Search
- Students can search within chapter content
- Search returns relevant sections with highlights
- Search is keyword-based (Phase 1, no semantic search)

### FR-4: Content Integrity
- Content cannot be modified by students
- Content is served from trusted source (database/R2)
- Content includes proper attribution and licensing

## 3. Technical Requirements

### TR-1: Data Storage
- Chapters stored in PostgreSQL database (Supabase)
- Large content (images, diagrams) stored in Cloudflare R2
- Content cached for performance (Redis, Phase 2)

### TR-2: API Performance
- Chapter load time < 500ms (p95)
- Support concurrent users (1000+ simultaneous)
- Implement pagination for long chapters

### TR-3: Access Control
- Check user subscription status before serving content
- Return 403 Forbidden for unauthorized access
- Log access attempts for analytics

### TR-4: Content Formatting
- Markdown content converted to HTML for web
- Plain text for ChatGPT app
- Code examples preserve formatting and syntax highlighting

## 4. API Contract

### GET /api/v1/chapters

**Description:** List all available chapters

**Request:**
```http
GET /api/v1/chapters
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "chapters": [
    {
      "id": 1,
      "title": "What is Generative AI?",
      "module": "Module 1",
      "chapter_number": 1,
      "is_free": true,
      "estimated_minutes": 15,
      "content_preview": "Generative AI refers to artificial intelligence...",
      "quiz_available": true
    },
    {
      "id": 2,
      "title": "Evolution of AI: From Discriminative to Generative",
      "module": "Module 1",
      "chapter_number": 2,
      "is_free": true,
      "estimated_minutes": 20,
      "content_preview": "AI has evolved from simple rule-based systems...",
      "quiz_available": true
    }
  ],
  "total_chapters": 24,
  "user_access": {
    "is_premium": false,
    "accessible_chapters": [1, 2, 3, 4]
  }
}
```

### GET /api/v1/chapters/{chapter_id}

**Description:** Get full chapter content

**Request:**
```http
GET /api/v1/chapters/1
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "chapter": {
    "id": 1,
    "title": "What is Generative AI?",
    "module": "Module 1",
    "chapter_number": 1,
    "is_free": true,
    "estimated_minutes": 15,
    "content": "# What is Generative AI?\n\nGenerative AI refers to artificial intelligence systems that can generate new content...\n\n## Key Concepts\n\n### Code Example\n```python\n# Example code here\n```\n\n## Summary\n\nKey takeaways...",
    "sections": [
      {
        "id": "section-1",
        "title": "Introduction",
        "content": "..."
      },
      {
        "id": "section-2",
        "title": "Key Concepts",
        "content": "..."
      }
    ],
    "images": [
      {
        "url": "https://r2.example.com/chapter-1/diagram-1.png",
        "alt": "Generative AI workflow diagram",
        "caption": "Figure 1.1: How generative AI works"
      }
    ],
    "code_examples": [
      {
        "language": "python",
        "code": "# Example code",
        "description": "Simple example"
      }
    ],
    "previous_chapter_id": null,
    "next_chapter_id": 2,
    "quiz_id": 1,
    "created_at": "2026-03-29T00:00:00Z",
    "updated_at": "2026-03-29T00:00:00Z"
  }
}
```

**Error Response (403 Forbidden):**
```json
{
  "error": "access_denied",
  "message": "This chapter requires premium access",
  "chapter_id": 5,
  "is_free": false,
  "upgrade_url": "/pricing"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "chapter_not_found",
  "message": "Chapter with ID 999 does not exist",
  "chapter_id": 999
}
```

### GET /api/v1/chapters/{chapter_id}/sections/{section_id}

**Description:** Get specific section of a chapter

**Request:**
```http
GET /api/v1/chapters/1/sections/introduction
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "section": {
    "id": "introduction",
    "chapter_id": 1,
    "title": "Introduction",
    "content": "Generative AI refers to...",
    "order": 1,
    "word_count": 250
  }
}
```

### GET /api/v1/search

**Description:** Search across all chapter content

**Request:**
```http
GET /api/v1/search?q=transformer+architecture&limit=10
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "query": "transformer architecture",
  "total_results": 15,
  "results": [
    {
      "chapter_id": 6,
      "chapter_title": "How LLMs Work: Transformers Architecture",
      "section_id": "section-2",
      "section_title": "Self-Attention Mechanism",
      "excerpt": "The transformer architecture uses self-attention to process all words simultaneously...",
      "relevance_score": 0.95,
      "is_free": false,
      "highlights": ["transformer architecture", "self-attention"]
    },
    {
      "chapter_id": 5,
      "chapter_title": "What are LLMs?",
      "section_id": "section-3",
      "section_title": "Model Architecture",
      "excerpt": "LLMs are built on transformer architecture, which revolutionized NLP...",
      "relevance_score": 0.87,
      "is_free": false,
      "highlights": ["transformer", "architecture"]
    }
  ],
  "search_metadata": {
    "search_type": "keyword",
    "execution_time_ms": 45
  }
}
```

## 5. User Stories

### US-1: Free User Accessing Free Chapter
**As a** free user  
**I want** to read Chapter 1  
**So that** I can evaluate the course quality before purchasing premium

**Acceptance Criteria:**
- [ ] Can access chapter list
- [ ] Can see Chapters 1-4 marked as free
- [ ] Can read full content of Chapter 1
- [ ] Content displays correctly with formatting

### US-2: Free User Accessing Premium Chapter
**As a** free user  
**I want** to know when I'm trying to access premium content  
**So that** I understand why I can't access it

**Acceptance Criteria:**
- [ ] See clear message that chapter requires premium
- [ ] See upgrade option/pricing information
- [ ] Cannot view chapter content
- [ ] Receive 403 error (not 404)

### US-3: Premium User Accessing Any Chapter
**As a** premium user  
**I want** to access any chapter instantly  
**So that** I can learn at my own pace

**Acceptance Criteria:**
- [ ] All 24 chapters accessible
- [ ] No access denied messages
- [ ] Content loads in < 500ms
- [ ] Can navigate between chapters

### US-4: Student Searching for Topic
**As a** student  
**I want** to search for specific topics  
**So that** I can find relevant content quickly

**Acceptance Criteria:**
- [ ] Search returns relevant results
- [ ] Results show chapter and section titles
- [ ] Excerpts highlight search terms
- [ ] Can click to navigate to content

### US-5: Student Reading on Mobile
**As a** mobile user  
**I want** content to be readable on small screens  
**So that** I can learn on the go

**Acceptance Criteria:**
- [ ] Content is responsive
- [ ] Code examples are scrollable
- [ ] Images scale properly
- [ ] Text is legible without zooming

## 6. Acceptance Criteria

### Functional Tests
- [ ] Free user can access Chapters 1-4
- [ ] Free user cannot access Chapters 5-24
- [ ] Premium user can access all chapters
- [ ] Chapter content displays verbatim (no modifications)
- [ ] Search returns relevant results
- [ ] Search respects access control (doesn't show premium content to free users)
- [ ] Navigation links (next/previous) work correctly
- [ ] Images load correctly from R2
- [ ] Code examples preserve formatting

### Non-Functional Tests
- [ ] API response time < 500ms (p95)
- [ ] Support 1000+ concurrent users
- [ ] Content is cached appropriately
- [ ] API is rate-limited (100 req/min per user)
- [ ] Proper error handling for all edge cases

## 7. Dependencies

### Internal Dependencies
- SPEC-T-001-database-schema-v1.0.md (chapter storage)
- SPEC-T-002-auth-architecture-v1.0.md (user authentication)
- SPEC-A-004-auth-apis-v1.0.md (JWT validation)

### External Dependencies
- Supabase (PostgreSQL database)
- Cloudflare R2 (content storage)
- OpenAI Apps SDK (ChatGPT integration)

## 8. Out of Scope

This spec does NOT cover:
- Content generation or editing (content is pre-created)
- Content recommendations (Phase 2 feature)
- Adaptive content delivery (Phase 2 feature)
- Content summarization (violates Zero-Backend-LLM)
- Video or audio content (text-only in Phase 1)
- Downloadable content (streaming only)
- Offline access (requires internet)

## 9. Testing Requirements

### Test Scenarios

#### Test 1: Free User Accessing Free Chapter
```python
def test_content_delivery_free_user_can_access_chapter_1():
    """Free user should successfully access Chapter 1"""
    # Arrange: Create free user, get chapter 1
    # Act: GET /api/v1/chapters/1
    # Assert: 200 OK, content returned, is_free=True
```

#### Test 2: Free User Denied Premium Chapter
```python
def test_content_delivery_free_user_cannot_access_chapter_5():
    """Free user should be denied access to Chapter 5"""
    # Arrange: Create free user, get chapter 5
    # Act: GET /api/v1/chapters/5
    # Assert: 403 Forbidden, error message, upgrade_url
```

#### Test 3: Premium User Accessing Premium Chapter
```python
def test_content_delivery_premium_user_can_access_chapter_10():
    """Premium user should successfully access Chapter 10"""
    # Arrange: Create premium user, get chapter 10
    # Act: GET /api/v1/chapters/10
    # Assert: 200 OK, full content returned
```

#### Test 4: Search Returns Relevant Results
```python
def test_content_delivery_search_returns_relevant_results():
    """Search should return chapters containing search terms"""
    # Arrange: Index chapters, search for "transformer"
    # Act: GET /api/v1/search?q=transformer
    # Assert: Results contain relevant chapters, relevance scores
```

#### Test 5: Search Respects Access Control
```python
def test_content_delivery_search_respects_access_control():
    """Search should not show premium content to free users"""
    # Arrange: Create free user, search for term in premium chapter
    # Act: GET /api/v1/search?q=advanced-topic
    # Assert: Premium chapters not in results, or marked as inaccessible
```

#### Test 6: Chapter Not Found
```python
def test_content_delivery_chapter_not_found():
    """Request for non-existent chapter should return 404"""
    # Arrange: Valid auth, chapter_id=999
    # Act: GET /api/v1/chapters/999
    # Assert: 404 Not Found, error message
```

#### Test 7: Navigation Links Correct
```python
def test_content_delivery_navigation_links_correct():
    """Chapter should have correct next/previous links"""
    # Arrange: Get chapter 5
    # Act: Check response
    # Assert: previous_chapter_id=4, next_chapter_id=6
```

### Coverage Requirements
- Minimum 90% code coverage
- All API endpoints tested
- All error scenarios tested
- Access control tested thoroughly

## 10. Open Questions

1. **Content Chunking:** Should we split long chapters into smaller sections for better mobile reading?
2. **Image Optimization:** Should we serve different image sizes based on device?
3. **Content Versioning:** Should we support content updates and track which version a student read?
4. **Reading Progress:** Should we track which sections a student has read within a chapter?

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Content Delivery Spec (SPEC-F-001-content-delivery-v1.0)  
**Why:** Defines how course chapters are served to students (core Phase 1 feature)  
**Files Affected:** 
- `docs/specs/functional/SPEC-F-001-content-delivery-v1.0.md`

**Key Decisions:**
- Content served verbatim (no backend modifications)
- Free users: Chapters 1-4 (Module 1)
- Premium users: All 24 chapters
- Keyword-based search (Phase 1)
- Content in database, images in R2
- API response time < 500ms

**Do you approve this spec?** (Yes/No/Modify)

If approved, next step is to:
1. Create test file: `backend/tests/test_content_api.py`
2. Write failing tests
3. Implement minimum code to pass
4. Repeat until all tests pass
