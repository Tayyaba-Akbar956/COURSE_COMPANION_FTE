# SPEC-A-005-search-apis-v1.0

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

This spec defines the API contract for search endpoints including full-text search across chapter content, filtered search, and search suggestions.

## 2. API Endpoints

### 2.1 GET /api/v1/search

**Description:** Search across all chapter content

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | required | Search query |
| `limit` | integer | 10 | Max results (max 50) |
| `offset` | integer | 0 | Pagination offset |
| `module` | integer | null | Filter by module |
| `free_only` | boolean | false | Free content only |

**Request:**
```http
GET /api/v1/search?q=transformer+architecture&limit=10&module=2
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "query": "transformer architecture",
    "results": [
      {
        "type": "chapter_section",
        "chapter_id": 6,
        "chapter_title": "How LLMs Work: Transformers Architecture",
        "section_id": "section-2",
        "section_title": "Self-Attention Mechanism",
        "content": "The transformer architecture uses self-attention...",
        "excerpt": "The <mark>transformer</mark> <mark>architecture</mark> uses...",
        "relevance_score": 0.95,
        "is_free": false,
        "matched_terms": ["transformer", "architecture"],
        "url": "/chapters/6#section-2"
      }
    ],
    "total_results": 15,
    "returned_results": 1,
    "limit": 10,
    "offset": 0,
    "filters_applied": {
      "module": 2,
      "free_only": false
    },
    "search_metadata": {
      "search_type": "full_text",
      "execution_time_ms": 45
    }
  }
}
```

**Errors:** 400 (Missing Query), 401 (Unauthorized)

---

### 2.2 GET /api/v1/search/suggestions

**Description:** Get search suggestions (autocomplete)

**Query Parameters:** `q` (string, required), `limit` (integer, default 5)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "query": "trans",
    "suggestions": [
      {"text": "transformer architecture", "match_count": 12},
      {"text": "transformers in NLP", "match_count": 8},
      {"text": "translation models", "match_count": 5}
    ]
  }
}
```

---

### 2.3 GET /api/v1/search/advanced

**Description:** Advanced search with multiple filters

**Query Parameters:**
- `q` (string): Search query
- `in_title` (boolean): Search only in titles
- `in_content` (boolean): Search in content (default true)
- `in_code` (boolean): Search in code examples
- `chapter_ids` (array): Limit to specific chapters
- `date_from` (date): Filter by date

**Response (200 OK):** Similar to basic search with additional metadata

---

### 2.4 POST /api/v1/search/bulk

**Description:** Search for multiple queries at once

**Request Body:**
```json
{
  "queries": [
    {"q": "attention mechanism", "limit": 3},
    {"q": "RAG", "limit": 3}
  ]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "query": "attention mechanism",
        "results": [...]
      },
      {
        "query": "RAG",
        "results": [...]
      }
    ]
  }
}
```

---

## 3. Search Implementation

### 3.1 PostgreSQL Full-Text Search

```python
from sqlalchemy import func, text

async def search_content(query: str, limit: int = 10):
    """
    Search using PostgreSQL full-text search
    """
    # Create tsquery from search string
    tsquery = " & ".join(query.split())
    
    results = await db.execute(
        text("""
        SELECT 
            c.id as chapter_id,
            c.title as chapter_title,
            s.id as section_id,
            s.title as section_title,
            s.content,
            ts_rank(to_tsvector('english', s.content), to_tsquery(:query)) as relevance
        FROM chapters c
        JOIN chapter_sections s ON c.id = s.chapter_id
        WHERE to_tsvector('english', s.content) @@ to_tsquery(:query)
        ORDER BY relevance DESC
        LIMIT :limit
        """),
        {"query": tsquery, "limit": limit}
    )
    
    return results.fetchall()
```

### 3.2 Highlighting Matched Terms

```python
from sqlalchemy import func

async def search_with_highlights(query: str):
    """
    Search with highlighted matches
    """
    results = await db.execute(
        text("""
        SELECT 
            c.id,
            c.title,
            ts_headline('english', s.content, to_tsquery(:query), 
                        'StartSel=<mark>, StopSel=</mark>') as excerpt
        FROM chapters c
        JOIN chapter_sections s ON c.id = s.chapter_id
        WHERE to_tsvector('english', s.content) @@ to_tsquery(:query)
        """),
        {"query": query}
    )
    
    return results.fetchall()
```

---

## 4. Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| GET /search | 60 | per minute |
| GET /search/suggestions | 30 | per minute |
| GET /search/advanced | 30 | per minute |
| POST /search/bulk | 10 | per minute |

## 5. Testing Requirements

```python
def test_search_api_basic_search():
    """Should return relevant search results"""
    # Act: GET /api/v1/search?q=transformer
    # Assert: 200 OK, results with relevance scores

def test_search_api_missing_query():
    """Should return error for missing query"""
    # Act: GET /api/v1/search (no q parameter)
    # Assert: 400 Bad Request

def test_search_api_filters():
    """Should respect filters"""
    # Act: GET /api/v1/search?q=ai&module=1&free_only=true
    # Assert: Results filtered correctly

def test_search_api_suggestions():
    """Should return autocomplete suggestions"""
    # Act: GET /api/v1/search/suggestions?q=trans
    # Assert: 200 OK, suggestions array

def test_search_api_highlighting():
    """Should highlight matched terms"""
    # Act: GET /api/v1/search?q=transformer
    # Assert: Results contain <mark> tags

def test_search_api_rate_limiting():
    """Should rate limit excessive searches"""
    # Act: 61 search requests in 1 minute
    # Assert: 429 on 61st request
```

## 6. Open Questions

1. **Semantic Search:** Should we add embedding-based semantic search (Phase 2)?
2. **Search Analytics:** Should we track popular searches for content improvement?
3. **Spell Correction:** Should we implement "Did you mean...?" suggestions?
4. **Search History:** Should we save user's recent searches (privacy consideration)?

## 7. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Search APIs Spec (SPEC-A-005-search-apis-v1.0)  
**Why:** Defines search endpoints for finding content across the course  
**Files Affected:** `docs/specs/api/SPEC-A-005-search-apis-v1.0.md`

**Key Decisions:**
- PostgreSQL full-text search (Phase 1)
- Highlighting matched terms
- Search suggestions (autocomplete)
- Advanced search with filters
- Rate limiting to prevent abuse

**Do you approve?** (Yes/No/Modify)

---

## ✅ **ALL SPECS COMPLETE!**

### **Final Summary:**

| Category | Count | Status |
|----------|-------|--------|
| **Foundation Docs** | 4 | ✅ Complete |
| **Course Outline** | 1 | ✅ Complete |
| **Agent Skills** | 4 | ✅ Complete |
| **Phase 1 Feature Specs** | 6 | ✅ Complete |
| **Technical Specs** | 3 | ✅ Complete |
| **API Specs** | 5 | ✅ Complete |
| **TOTAL** | **23** | **✅ ALL COMPLETE** |

---

**🎉 READY FOR IMPLEMENTATION!**

All specifications are now complete and ready for your review and approval. Next steps:

1. **Review all specs** (23 documents in `docs/` folder)
2. **Approve specs** (or request modifications)
3. **Begin backend implementation** (FastAPI app, models, tests)

**What would you like to do next?**
