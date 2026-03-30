# SPEC-F-003-grounded-qa-v1.0

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

This spec defines the Grounded Q&A feature that enables students to ask questions about course content and receive answers based ONLY on the provided course material. The backend searches and retrieves relevant content, while ChatGPT formulates explanations using only that retrieved content.

**Critical Principle:** This is a Zero-Backend-LLM feature. The backend does NOT generate answers using LLM. It only retrieves relevant content. ChatGPT uses that content to answer.

## 2. Functional Requirements

### FR-1: Question Submission
- Students can ask questions about course content
- Questions can be typed or voice-to-text
- Questions are matched against course content

### FR-2: Content-Based Answers
- Answers are derived ONLY from course content
- If answer not in content, system says "not covered"
- Sources are cited (chapter and section references)
- Direct quotes are marked as quotes

### FR-3: Search and Retrieval
- Backend searches course content for relevant sections
- Keyword-based search (Phase 1, no semantic search)
- Returns top 3-5 most relevant sections
- Includes relevance scores

### FR-4: Answer Grounding
- Every answer includes source references
- Students can click to view original context
- Confidence level indicated (high/medium/low based on content match)
- Hallucination prevention: strict adherence to source material

### FR-5: Follow-Up Questions
- Students can ask follow-up questions in same session
- Context from previous question maintained
- Conversation history limited to current session (not persisted)

## 3. Technical Requirements

### TR-1: Search Implementation
- Keyword-based search using PostgreSQL full-text search
- Index all chapter content, titles, sections
- Support boolean operators (AND, OR, NOT)
- Support phrase matching (quoted searches)

### TR-2: Relevance Ranking
- Rank results by term frequency and location
- Title matches weighted higher than body matches
- Recent chapters weighted equally (no recency bias)
- Return relevance score (0.0 to 1.0)

### TR-3: Response Format
- Return relevant sections with context
- Include chapter title, section title, content excerpt
- Highlight matched terms
- Provide direct links to chapters

### TR-4: Performance
- Search response time < 300ms (p95)
- Support concurrent searches (1000+ per minute)
- Cache frequent queries (Phase 2)

### TR-5: Content Boundaries
- Strict enforcement: only course content
- No external knowledge injection
- No speculation beyond content
- Clear messaging when content not found

## 4. API Contract

### GET /api/v1/search/qa

**Description:** Search for answer to a question

**Request:**
```http
GET /api/v1/search/qa?q=What+is+the+attention+mechanism&limit=5
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "question": "What is the attention mechanism?",
  "results": [
    {
      "chapter_id": 6,
      "chapter_title": "How LLMs Work: Transformers Architecture",
      "section_id": "section-2",
      "section_title": "Self-Attention Mechanism",
      "content": "The attention mechanism is a technique that allows the model to weigh the importance of different words in a sequence when processing each word. For each word, the model creates three vectors: Query (Q), Key (K), and Value (V)...",
      "relevance_score": 0.95,
      "match_type": "keyword",
      "matched_terms": ["attention", "mechanism"],
      "is_free": false,
      "quote": "The attention mechanism is a technique that allows the model to weigh the importance of different words..."
    },
    {
      "chapter_id": 5,
      "chapter_title": "What are LLMs?",
      "section_id": "section-3",
      "section_title": "Model Architecture",
      "content": "LLMs use transformer architecture which includes attention mechanisms to process text...",
      "relevance_score": 0.82,
      "match_type": "keyword",
      "matched_terms": ["attention", "mechanism"],
      "is_free": false,
      "quote": "LLMs use transformer architecture which includes attention mechanisms..."
    }
  ],
  "search_metadata": {
    "total_results": 8,
    "returned_results": 5,
    "search_type": "keyword",
    "execution_time_ms": 45,
    "query_processed": "attention mechanism"
  },
  "answer_guidance": {
    "content_available": true,
    "covered_in_chapters": [5, 6],
    "recommended_chapter": 6,
    "confidence": "high"
  }
}
```

**Response (No Results):**
```json
{
  "question": "What is quantum computing?",
  "results": [],
  "search_metadata": {
    "total_results": 0,
    "returned_results": 0,
    "search_type": "keyword",
    "execution_time_ms": 32,
    "query_processed": "quantum computing"
  },
  "answer_guidance": {
    "content_available": false,
    "message": "This topic is not covered in the course content",
    "suggestion": "This course focuses on generative AI and LLMs. Quantum computing is a different field.",
    "confidence": "high"
  }
}
```

### POST /api/v1/search/qa

**Description:** Search with conversation context (follow-up questions)

**Request:**
```http
POST /api/v1/search/qa
Authorization: Bearer {user_token}
Content-Type: application/json

{
  "question": "How does it work?",
  "conversation_context": [
    {
      "role": "user",
      "content": "What is the attention mechanism?"
    },
    {
      "role": "assistant",
      "content": "Based on Chapter 6, the attention mechanism...",
      "sources": [{"chapter_id": 6, "section_id": "section-2"}]
    }
  ],
  "limit": 5
}
```

**Response (200 OK):**
```json
{
  "question": "How does it work?",
  "context_understanding": {
    "topic": "attention mechanism",
    "previous_chapter": 6
  },
  "results": [
    {
      "chapter_id": 6,
      "chapter_title": "How LLMs Work: Transformers Architecture",
      "section_id": "section-2",
      "section_title": "Self-Attention Mechanism",
      "content": "For each word, the model creates three vectors: Query (Q), Key (K), and Value (V). It calculates attention scores by comparing Q with all Ks, uses softmax to normalize scores, and creates a weighted sum of Vs based on scores...",
      "relevance_score": 0.93,
      "match_type": "contextual",
      "matched_terms": ["work", "mechanism", "vectors"],
      "is_free": false,
      "quote": "For each word, the model creates three vectors..."
    }
  ],
  "search_metadata": {
    "total_results": 5,
    "returned_results": 3,
    "search_type": "contextual_keyword",
    "execution_time_ms": 52,
    "query_processed": "attention mechanism how work"
  },
  "answer_guidance": {
    "content_available": true,
    "covered_in_chapters": [6],
    "recommended_chapter": 6,
    "confidence": "high",
    "context_maintained": true
  }
}
```

### GET /api/v1/chapters/{chapter_id}/faq

**Description:** Get frequently asked questions for a chapter

**Request:**
```http
GET /api/v1/chapters/6/faq
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "chapter_id": 6,
  "chapter_title": "How LLMs Work: Transformers Architecture",
  "faq": [
    {
      "question": "What is the attention mechanism?",
      "answer_source": {
        "section_id": "section-2",
        "excerpt": "The attention mechanism is a technique that allows..."
      },
      "asked_count": 145
    },
    {
      "question": "How do transformers differ from RNNs?",
      "answer_source": {
        "section_id": "section-1",
        "excerpt": "Transformers process all words simultaneously..."
      },
      "asked_count": 98
    },
    {
      "question": "What are Query, Key, and Value vectors?",
      "answer_source": {
        "section_id": "section-2",
        "excerpt": "For each word, the model creates three vectors..."
      },
      "asked_count": 87
    }
  ]
}
```

## 5. User Stories

### US-1: Student Asking About Concept
**As a** student reading Chapter 6  
**I want** to ask "What is the attention mechanism?"  
**So that** I can get a clear explanation from the course content

**Acceptance Criteria:**
- [ ] Question is understood and processed
- [ ] Relevant sections from Chapter 6 returned
- [ ] Source references included
- [ ] Answer grounded in content only

### US-2: Student Asking About Uncovered Topic
**As a** student  
**I want** to know if a topic is not covered  
**So that** I don't waste time looking for it

**Acceptance Criteria:**
- [ ] Clear message that topic not in course
- [ ] No hallucinated information
- [ ] Suggestion of related topics that ARE covered
- [ ] Polite, helpful tone

### US-3: Student Asking Follow-Up Question
**As a** student who just asked about attention  
**I want** to ask "How does it work?"  
**So that** I can get deeper understanding

**Acceptance Criteria:**
- [ ] "It" understood as "attention mechanism"
- [ ] Context from previous question maintained
- [ ] Answer builds on previous answer
- [ ] Same chapter referenced for consistency

### US-4: Student Verifying Source
**As a** student who received an answer  
**I want** to see the original context  
**So that** I can verify the answer is accurate

**Acceptance Criteria:**
- [ ] Chapter and section references clickable
- [ ] Can navigate to source instantly
- [ ] Highlighted text shows exact source
- [ ] Quote marked clearly

### US-5: Student Searching with Keywords
**As a** student  
**I want** to search using specific terms  
**So that** I can find exactly what I need

**Acceptance Criteria:**
- [ ] Keyword search works accurately
- [ ] Boolean operators supported (AND, OR, NOT)
- [ ] Phrase matching with quotes
- [ ] Results ranked by relevance

## 6. Acceptance Criteria

### Functional Tests
- [ ] Search returns relevant content for questions
- [ ] No results when topic not in course
- [ ] Source references always included
- [ ] Follow-up questions maintain context
- [ ] FAQ endpoint returns popular questions
- [ ] Relevance scores calculated correctly
- [ ] Matched terms highlighted
- [ ] Access control respected (no premium content to free users)

### Non-Functional Tests
- [ ] Search response time < 300ms (p95)
- [ ] Support 1000+ concurrent searches
- [ ] No hallucination in answers (content-only)
- [ ] Clear error messages when content not found
- [ ] Conversation context limited to session (not persisted)

## 7. Dependencies

### Internal Dependencies
- SPEC-F-001-content-delivery-v1.0.md (content access)
- SPEC-T-001-database-schema-v1.0.md (search indexing)
- SPEC-A-001-content-apis-v1.0.md (content retrieval)

### External Dependencies
- Supabase PostgreSQL (full-text search)
- Database indexes for performance

## 8. Out of Scope

This spec does NOT cover:
- LLM-based answer generation (violates Zero-Backend-LLM)
- Semantic search / embeddings (Phase 2)
- Persistent conversation history (privacy)
- Voice search (text-only in Phase 1)
- Multi-language support (English only in Phase 1)
- Image-based questions (text-only)
- External knowledge integration (course content only)
- RAG with LLM (Phase 2 hybrid feature)

## 9. Testing Requirements

### Test Scenarios

#### Test 1: Search Returns Relevant Content
```python
def test_grounded_qa_search_returns_relevant_content():
    """Search for 'attention mechanism' should return Chapter 6"""
    # Arrange: Index course content
    # Act: GET /api/v1/search/qa?q=attention+mechanism
    # Assert: Results include Chapter 6, high relevance score
```

#### Test 2: Search Returns No Results for Uncovered Topic
```python
def test_grounded_qa_no_results_for_uncovered_topic():
    """Search for 'quantum computing' should return no results"""
    # Arrange: Index course content
    # Act: GET /api/v1/search/qa?q=quantum+computing
    # Assert: Empty results, clear message, no hallucination
```

#### Test 3: Follow-Up Question Maintains Context
```python
def test_grounded_qa_followup_maintains_context():
    """Follow-up question should understand 'it' refers to previous topic"""
    # Arrange: Previous question about attention mechanism
    # Act: POST /api/v1/search/qa with conversation context
    # Assert: Results about attention mechanism, context maintained
```

#### Test 4: Source References Included
```python
def test_grounded_qa_source_references_included():
    """Every result should include chapter and section references"""
    # Arrange: Search for common term
    # Act: GET /api/v1/search/qa?q=transformer
    # Assert: All results have chapter_id, section_id, content excerpt
```

#### Test 5: Free User Does Not See Premium Content
```python
def test_grounded_qa_free_user_no_premium_content():
    """Free user search should not return premium content"""
    # Arrange: Free user, search for term in premium chapter
    # Act: GET /api/v1/search/qa?q=advanced-topic
    # Assert: Premium chapters not in results, or marked inaccessible
```

#### Test 6: Relevance Scoring Correct
```python
def test_grounded_qa_relevance_scoring_correct():
    """Results should be ranked by relevance"""
    # Arrange: Multiple chapters contain search term
    # Act: GET /api/v1/search/qa?q=attention
    # Assert: Results ordered by relevance_score (descending)
```

#### Test 7: FAQ Returns Popular Questions
```python
def test_grounded_qa_faq_returns_popular_questions():
    """FAQ endpoint should return frequently asked questions"""
    # Arrange: Chapter 6 has FAQ data
    # Act: GET /api/v1/chapters/6/faq
    # Assert: Returns questions with ask_count, sorted by popularity
```

#### Test 8: Boolean Search Operators Work
```python
def test_grounded_qa_boolean_operators_work():
    """Search should support AND, OR, NOT operators"""
    # Arrange: Indexed content
    # Act: GET /api/v1/search/qa?q=attention+AND+mechanism
    # Assert: Results match boolean logic
```

### Coverage Requirements
- Minimum 90% code coverage
- All search endpoints tested
- Edge cases (no results, single result) tested
- Context maintenance tested
- Access control tested

## 10. Open Questions

1. **Query Processing:** Should we implement query expansion (synonyms) in Phase 1?
2. **Result Snippet Length:** How much context should we return per result (100, 200, 500 chars)?
3. **Conversation History:** How many previous messages should we maintain in context (3, 5, 10)?
4. **Typo Tolerance:** Should we implement fuzzy matching for misspelled terms?
5. **FAQ Generation:** Should FAQs be manually curated or generated from search logs (Phase 2)?

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Grounded Q&A Spec (SPEC-F-003-grounded-qa-v1.0)  
**Why:** Defines how students ask questions and get answers from course content (core Phase 1 feature)  
**Files Affected:** 
- `docs/specs/functional/SPEC-F-003-grounded-qa-v1.0.md`

**Key Decisions:**
- Zero-Backend-LLM: Backend only retrieves content, doesn't generate answers
- Keyword-based search (Phase 1, PostgreSQL full-text search)
- Source references always included
- Follow-up questions maintain session context (not persisted)
- Clear messaging when content not found (no hallucination)
- FAQ endpoint for popular questions per chapter

**Do you approve this spec?** (Yes/No/Modify)

If approved, next step is to:
1. Create test file: `backend/tests/test_grounded_qa_api.py`
2. Write failing tests
3. Implement minimum code to pass
4. Repeat until all tests pass
