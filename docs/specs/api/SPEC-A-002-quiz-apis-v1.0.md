# SPEC-A-002-quiz-apis-v1.0

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

This spec defines the API contract for quiz-related endpoints including getting quiz questions, submitting answers, grading, and viewing quiz history.

## 2. API Endpoints

### 2.1 GET /api/v1/chapters/{chapter_id}/quiz

**Description:** Get quiz for a chapter (starts quiz session)

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "quiz": {
      "quiz_id": "quiz-session-12345",
      "chapter_id": 5,
      "chapter_title": "What are LLMs?",
      "total_questions": 5,
      "passing_score": 80,
      "questions": [
        {
          "question_id": 1,
          "question_text": "What does LLM stand for?",
          "options": [
            {"id": "A", "text": "Large Language Model"},
            {"id": "B", "text": "Linear Learning Machine"},
            {"id": "C", "text": "Logical Language Module"},
            {"id": "D", "text": "Layered Learning Model"}
          ],
          "question_number": 1
        }
      ]
    }
  }
}
```

**Errors:** 401 (Unauthorized), 403 (Chapter Not Completed), 404 (Not Found)

---

### 2.2 POST /api/v1/quizzes/{quiz_id}/submit

**Description:** Submit quiz answers for grading

**Request Body:**
```json
{
  "answers": [
    {"question_id": 1, "answer": "A"},
    {"question_id": 2, "answer": "B"}
  ]
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "quiz_result": {
      "quiz_id": "quiz-session-12345",
      "score": 80,
      "total_questions": 5,
      "correct_answers": 4,
      "passed": true,
      "answers": [
        {
          "question_id": 1,
          "student_answer": "A",
          "correct_answer": "A",
          "is_correct": true,
          "explanation": "LLM stands for Large Language Model..."
        }
      ],
      "feedback": {
        "overall": "Great job! You passed with 80%.",
        "recommendation": "Review Section 3 for better understanding."
      }
    }
  }
}
```

**Errors:** 400 (Incomplete Answers), 401 (Unauthorized), 404 (Quiz Not Found)

---

### 2.3 GET /api/v1/quizzes/{quiz_id}/results

**Description:** Get results of a previously taken quiz

**Response (200 OK):** Same structure as submit response

**Errors:** 401 (Unauthorized), 404 (Results Not Found)

---

### 2.4 GET /api/v1/chapters/{chapter_id}/quiz/history

**Description:** Get quiz attempt history for a chapter

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "chapter_id": 5,
    "total_attempts": 3,
    "best_score": 100,
    "average_score": 93.3,
    "attempts": [
      {"quiz_id": "...", "score": 80, "passed": true, "attempt_number": 1, "submitted_at": "..."}
    ]
  }
}
```

---

### 2.5 POST /api/v1/quizzes/practice

**Description:** Get practice mode quiz (score not recorded)

**Request Body:** `{"chapter_id": 5, "question_count": 5}`

**Response (200 OK):** Similar to GET /chapters/{id}/quiz, but marked as practice

---

## 3. Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| GET /chapters/{id}/quiz | 30 | per minute |
| POST /quizzes/{id}/submit | 10 | per minute (anti-cheating) |
| GET /quizzes/{id}/results | 60 | per minute |

## 4. Testing Requirements

```python
def test_quiz_api_get_quiz():
    """Should return quiz with random questions"""
    # Act: GET /api/v1/chapters/5/quiz
    # Assert: 200 OK, 5 questions from bank

def test_quiz_api_submit_and_grade():
    """Should grade quiz using answer key"""
    # Act: POST /api/v1/quizzes/{id}/submit
    # Assert: 200 OK, score calculated correctly

def test_quiz_api_retake_different_questions():
    """Retake should have different questions"""
    # Act: Take quiz twice
    # Assert: Different questions selected

def test_quiz_api_history_recorded():
    """All attempts should be in history"""
    # Act: Take quiz 3 times
    # Assert: 3 attempts in history

def test_quiz_api_practice_mode():
    """Practice quiz should not be recorded"""
    # Act: Take practice quiz
    # Assert: Not in history
```

## 5. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Quiz APIs Spec (SPEC-A-002-quiz-apis-v1.0)  
**Why:** Defines quiz endpoints for testing student understanding  
**Files Affected:** `docs/specs/api/SPEC-A-002-quiz-apis-v1.0.md`

**Key Decisions:**
- Random question selection from bank
- Rule-based grading (answer key)
- Unlimited retakes with different questions
- Practice mode available
- Rate limiting on submissions (anti-cheating)

**Do you approve?** (Yes/No/Modify)

---

**Progress:** API Specs: 2/5 Complete. Remaining: A-003, A-004, A-005
