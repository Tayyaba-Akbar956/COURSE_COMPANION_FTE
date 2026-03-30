# SPEC-F-004-rule-based-quizzes-v1.0

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

This spec defines the Rule-Based Quizzes feature that enables students to test their understanding with multiple-choice quizzes. All grading is done using answer keys (rule-based, no LLM), with immediate feedback and detailed explanations.

## 2. Functional Requirements

### FR-1: Quiz Access
- Each chapter has an associated quiz (5-10 questions)
- Quizzes accessible after reading chapter
- Students can retake quizzes unlimited times
- All quiz attempts are recorded

### FR-2: Question Types
- Multiple-choice questions (4 options: A, B, C, D)
- Single correct answer per question
- Questions include explanations for all options
- Questions tagged by difficulty (easy, medium, hard)

### FR-3: Quiz Taking
- Questions presented one at a time OR all at once (user preference)
- Students can skip questions and return later
- Progress indicator shows questions answered/total
- Timer optional (not enforced in Phase 1)

### FR-4: Grading
- Automatic grading using answer key (rule-based)
- Immediate feedback after each question OR at end (user preference)
- Score calculated as percentage (correct/total × 100)
- Passing score: 80% (configurable per chapter)

### FR-5: Feedback
- Correct answers: explanation of why correct
- Incorrect answers: explanation of correct answer + why other options wrong
- Source references to chapter sections
- Overall quiz feedback based on score

### FR-6: Quiz Results
- Results screen shows all questions with student answers
- Correct answers highlighted
- Score displayed prominently
- Option to review incorrect answers
- Option to retake quiz

### FR-7: Quiz Bank
- Each chapter has 10-15 questions in bank
- Quiz randomly selects 5-10 questions per attempt
- Different questions on each retake (from same bank)
- Prevents memorization of answers

## 3. Technical Requirements

### TR-1: Data Storage
- Questions stored in PostgreSQL database
- Quiz attempts stored with timestamp, score, answers
- Question bank associated with chapters
- Results linked to user accounts

### TR-2: Randomization
- Questions randomly selected from bank for each attempt
- Answer options shuffled (A, B, C, D order randomized)
- Seed-based randomization for reproducibility if needed
- No duplicate questions in single quiz

### TR-3: Grading Logic
- Simple answer key comparison (no LLM)
- Exact match required (no partial credit in Phase 1)
- Grading happens server-side (not client)
- Audit trail of all graded attempts

### TR-4: Performance
- Quiz load time < 300ms
- Grading instant (< 100ms)
- Results available immediately after submission
- Support 1000+ concurrent quiz takers

### TR-5: Security
- Quiz questions not exposed in API until quiz started
- Answers validated server-side
- Prevent quiz scraping (rate limiting)
- Attempt limits per hour (anti-cheating, 10 attempts/hour max)

## 4. API Contract

### GET /api/v1/chapters/{chapter_id}/quiz

**Description:** Get quiz for a chapter (starts quiz session)

**Request:**
```http
GET /api/v1/chapters/5/quiz
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "quiz": {
    "quiz_id": "quiz-session-12345",
    "chapter_id": 5,
    "chapter_title": "What are LLMs?",
    "total_questions": 5,
    "time_limit_minutes": null,
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
      },
      {
        "question_id": 2,
        "question_text": "Which company introduced the transformer architecture?",
        "options": [
          {"id": "A", "text": "OpenAI"},
          {"id": "B", "text": "Google"},
          {"id": "C", "text": "Meta"},
          {"id": "D", "text": "Microsoft"}
        ],
        "question_number": 2
      }
      // ... 3 more questions
    ],
    "instructions": "Answer all questions. You need 80% to pass.",
    "created_at": "2026-03-29T10:00:00Z",
    "expires_at": "2026-03-29T11:00:00Z"
  }
}
```

**Response (403 Forbidden - Chapter Not Completed):**
```json
{
  "error": "chapter_not_completed",
  "message": "Please complete Chapter 5 before taking the quiz",
  "chapter_id": 5,
  "chapter_completed": false
}
```

### POST /api/v1/quizzes/{quiz_id}/submit

**Description:** Submit quiz answers for grading

**Request:**
```http
POST /api/v1/quizzes/quiz-session-12345/submit
Authorization: Bearer {user_token}
Content-Type: application/json

{
  "answers": [
    {"question_id": 1, "answer": "A"},
    {"question_id": 2, "answer": "B"},
    {"question_id": 3, "answer": "C"},
    {"question_id": 4, "answer": "A"},
    {"question_id": 5, "answer": "D"}
  ]
}
```

**Response (200 OK):**
```json
{
  "quiz_result": {
    "quiz_id": "quiz-session-12345",
    "chapter_id": 5,
    "user_id": "user123",
    "score": 80,
    "total_questions": 5,
    "correct_answers": 4,
    "incorrect_answers": 1,
    "passed": true,
    "passing_score": 80,
    "submitted_at": "2026-03-29T10:15:00Z",
    "time_taken_seconds": 180,
    "attempt_number": 1,
    "answers": [
      {
        "question_id": 1,
        "question_text": "What does LLM stand for?",
        "student_answer": "A",
        "correct_answer": "A",
        "is_correct": true,
        "explanation": "LLM stands for Large Language Model. These are AI models trained on massive amounts of text data.",
        "source_reference": "Chapter 5, Section 1"
      },
      {
        "question_id": 2,
        "question_text": "Which company introduced the transformer architecture?",
        "student_answer": "B",
        "correct_answer": "B",
        "is_correct": true,
        "explanation": "Google introduced the transformer architecture in their 2017 paper 'Attention Is All You Need'.",
        "source_reference": "Chapter 5, Section 2"
      },
      {
        "question_id": 3,
        "question_text": "What is the primary advantage of transformers over RNNs?",
        "student_answer": "C",
        "correct_answer": "A",
        "is_correct": false,
        "explanation": "The correct answer is A) Parallel processing. Transformers can process all words simultaneously, unlike RNNs which process sequentially.",
        "why_wrong": "While transformers do handle long sequences better (option C), the PRIMARY advantage is parallel processing which makes them much faster to train.",
        "source_reference": "Chapter 5, Section 3"
      }
      // ... more answers
    ],
    "feedback": {
      "overall": "Great job! You passed the quiz with 80%. You have a solid understanding of LLMs.",
      "strengths": ["Basic concepts", "Terminology"],
      "areas_to_review": ["Transformer advantages"],
      "recommendation": "Review Section 3 of Chapter 5 to understand transformer advantages better."
    },
    "next_steps": {
      "can_continue": true,
      "next_chapter_id": 6,
      "retake_available": true,
      "retake_available_at": "2026-03-29T11:15:00Z"
    }
  }
}
```

**Response (400 Bad Request - Incomplete Answers):**
```json
{
  "error": "incomplete_answers",
  "message": "You must answer all 5 questions before submitting",
  "answered": 3,
  "total": 5,
  "missing_question_ids": [4, 5]
}
```

### GET /api/v1/quizzes/{quiz_id}/results

**Description:** Get results of a previously taken quiz

**Request:**
```http
GET /api/v1/quizzes/quiz-session-12345/results
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "quiz_result": {
    // Same structure as submit response
  }
}
```

### GET /api/v1/chapters/{chapter_id}/quiz/history

**Description:** Get quiz attempt history for a chapter

**Request:**
```http
GET /api/v1/chapters/5/quiz/history
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "chapter_id": 5,
  "chapter_title": "What are LLMs?",
  "total_attempts": 3,
  "best_score": 100,
  "latest_score": 100,
  "average_score": 93.3,
  "passed": true,
  "attempts": [
    {
      "quiz_id": "quiz-session-12345",
      "score": 80,
      "passed": true,
      "attempt_number": 1,
      "submitted_at": "2026-03-29T10:15:00Z",
      "time_taken_seconds": 180
    },
    {
      "quiz_id": "quiz-session-12389",
      "score": 100,
      "passed": true,
      "attempt_number": 2,
      "submitted_at": "2026-03-29T14:30:00Z",
      "time_taken_seconds": 150
    }
  ]
}
```

### POST /api/v1/quizzes/practice

**Description:** Get practice mode quiz (no score recorded)

**Request:**
```http
POST /api/v1/quizzes/practice
Authorization: Bearer {user_token}
Content-Type: application/json

{
  "chapter_id": 5,
  "question_count": 5
}
```

**Response (200 OK):**
```json
{
  "quiz": {
    "quiz_id": "practice-session-67890",
    "is_practice": true,
    "chapter_id": 5,
    // ... same structure as regular quiz
  }
}
```

## 5. User Stories

### US-1: Student Taking Chapter Quiz
**As a** student who finished Chapter 5  
**I want** to take the quiz to test my understanding  
**So that** I can verify I learned the material

**Acceptance Criteria:**
- [ ] Quiz accessible after chapter completion
- [ ] 5 questions presented clearly
- [ ] Can select one answer per question
- [ ] Can review answers before submitting
- [ ] Submit button enabled when all answered

### US-2: Student Receiving Quiz Feedback
**As a** student who just submitted a quiz  
**I want** to see which answers were correct/incorrect  
**So that** I can learn from my mistakes

**Acceptance Criteria:**
- [ ] Score displayed prominently
- [ ] Each question shows student answer and correct answer
- [ ] Explanations provided for all questions
- [ ] Source references to chapter sections
- [ ] Overall feedback based on performance

### US-3: Student Failing Quiz
**As a** student who scored below 80%  
**I want** to know I can retake the quiz  
**So that** I can improve my score

**Acceptance Criteria:**
- [ ] Clear message that quiz not passed
- [ ] Retake option available
- [ ] Cooldown period explained (if any)
- [ ] Specific areas to review identified
- [ ] Encouraging, not discouraging tone

### US-4: Student Retaking Quiz
**As a** student retaking a quiz  
**I want** different questions than last time  
**So that** I'm tested on broader knowledge

**Acceptance Criteria:**
- [ ] Questions randomly selected from bank
- [ ] No duplicate questions from previous attempt
- [ ] Same difficulty level maintained
- [ ] New quiz session created

### US-5: Student Using Practice Mode
**As a** student preparing for quiz  
**I want** to practice with sample questions  
**So that** I can gauge my readiness

**Acceptance Criteria:**
- [ ] Practice mode available
- [ ] Questions from same bank as real quiz
- [ ] Score not recorded in history
- [ ] Unlimited practice attempts
- [ ] Immediate feedback per question

### US-6: Student Viewing Quiz History
**As a** student  
**I want** to see all my quiz attempts  
**So that** I can track my improvement

**Acceptance Criteria:**
- [ ] History shows all attempts
- [ ] Scores visible for each attempt
- [ ] Best score highlighted
- [ ] Trend visible (improving/declining)
- [ ] Can review individual attempt details

## 6. Acceptance Criteria

### Functional Tests
- [ ] Quiz loads with correct number of questions
- [ ] Questions randomly selected from bank
- [ ] Answer options shuffled
- [ ] Grading uses answer key (rule-based)
- [ ] Score calculated correctly
- [ ] Feedback includes explanations
- [ ] Quiz history recorded
- [ ] Retake generates new questions
- [ ] Practice mode doesn't record scores
- [ ] Passing score enforced (80%)

### Non-Functional Tests
- [ ] Quiz loads in < 300ms
- [ ] Grading instant (< 100ms)
- [ ] Support 1000+ concurrent quiz takers
- [ ] Rate limiting prevents abuse (10 attempts/hour)
- [ ] Quiz questions not exposed before start
- [ ] Answers validated server-side

## 7. Dependencies

### Internal Dependencies
- SPEC-F-001-content-delivery-v1.0.md (chapter access)
- SPEC-F-005-progress-tracking-v1.0.md (quiz completion tracking)
- SPEC-T-001-database-schema-v1.0.md (quiz data storage)

### External Dependencies
- Supabase PostgreSQL (quiz data storage)
- Random number generation (secure)

## 8. Out of Scope

This spec does NOT cover:
- LLM-graded assessments (Phase 2 hybrid feature)
- Open-ended questions (multiple-choice only in Phase 1)
- Partial credit (all-or-nothing in Phase 1)
- Timed quizzes with auto-submit (optional timer only)
- Question difficulty adaptation (Phase 2)
- Peer review of answers (Phase 3)
- Certificates based on quiz performance (Phase 3)
- Question creation by instructors (content pre-created)

## 9. Testing Requirements

### Test Scenarios

#### Test 1: Quiz Loads Correctly
```python
def test_quiz_loads_correctly():
    """Quiz should load with 5 random questions from bank"""
    # Arrange: Chapter 5 has 15 questions in bank
    # Act: GET /api/v1/chapters/5/quiz
    # Assert: Returns 5 questions, random selection, options shuffled
```

#### Test 2: Quiz Grading Correct
```python
def test_quiz_grading_correct():
    """Quiz should be graded correctly using answer key"""
    # Arrange: Submit quiz with 4 correct, 1 incorrect
    # Act: POST /api/v1/quizzes/{id}/submit
    # Assert: Score = 80%, passed = true, correct feedback
```

#### Test 3: Quiz Grading All Wrong
```python
def test_quiz_grading_all_wrong():
    """Quiz with all wrong answers should score 0%"""
    # Arrange: Submit quiz with all incorrect answers
    # Act: POST /api/v1/quizzes/{id}/submit
    # Assert: Score = 0%, passed = false, encouraging feedback
```

#### Test 4: Quiz Retake Different Questions
```python
def test_quiz_retake_different_questions():
    """Quiz retake should have different questions"""
    # Arrange: Take quiz, get questions A, B, C, D, E
    # Act: Retake quiz
    # Assert: Different questions (at least 3 different)
```

#### Test 5: Quiz History Recorded
```python
def test_quiz_history_recorded():
    """All quiz attempts should be recorded in history"""
    # Arrange: Take quiz 3 times
    # Act: GET /api/v1/chapters/5/quiz/history
    # Assert: 3 attempts in history, correct scores, timestamps
```

#### Test 6: Practice Mode Not Recorded
```python
def test_quiz_practice_mode_not_recorded():
    """Practice quiz should not be recorded in history"""
    # Arrange: Take practice quiz
    # Act: Check history
    # Assert: Practice attempt not in history
```

#### Test 7: Incomplete Answers Rejected
```python
def test_quiz_incomplete_answers_rejected():
    """Quiz submission with missing answers should be rejected"""
    # Arrange: Submit quiz with only 3 of 5 answers
    # Act: POST /api/v1/quizzes/{id}/submit
    # Assert: 400 Bad Request, error message, missing question IDs
```

#### Test 8: Chapter Not Completed Blocked
```python
def test_quiz_chapter_not_completed_blocked():
    """Quiz should be blocked if chapter not completed"""
    # Arrange: User hasn't completed chapter 5
    # Act: GET /api/v1/chapters/5/quiz
    # Assert: 403 Forbidden, message to complete chapter first
```

### Coverage Requirements
- Minimum 90% code coverage
- All quiz endpoints tested
- Grading logic thoroughly tested
- Edge cases (0%, 100%, boundary scores) tested
- Rate limiting tested

## 10. Open Questions

1. **Passing Score:** Should 80% be configurable per chapter or global?
2. **Retake Cooldown:** Should there be a cooldown period between retakes (1 hour, 24 hours, none)?
3. **Best Score Tracking:** Should we track best score or latest score for progress?
4. **Question Exposure:** Should students see correct answers immediately after each question or only at end?
5. **Quiz Bank Size:** How many questions per chapter bank (10, 15, 20)?

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Rule-Based Quizzes Spec (SPEC-F-004-rule-based-quizzes-v1.0)  
**Why:** Defines how students test their understanding with quizzes (core Phase 1 feature)  
**Files Affected:** 
- `docs/specs/functional/SPEC-F-004-rule-based-quizzes-v1.0.md`

**Key Decisions:**
- Multiple-choice only (4 options, single correct answer)
- Rule-based grading using answer key (no LLM)
- 80% passing score (configurable)
- Random question selection from bank (10-15 questions per chapter)
- Unlimited retakes with different questions
- Practice mode available (scores not recorded)
- Immediate feedback with explanations

**Do you approve this spec?** (Yes/No/Modify)

If approved, next step is to:
1. Create test file: `backend/tests/test_quiz_api.py`
2. Write failing tests
3. Implement minimum code to pass
4. Repeat until all tests pass

---

**Progress:** 4 of 6 Phase 1 feature specs complete! Remaining: SPEC-F-005 (Progress Tracking), SPEC-F-006 (Freemium Gate)
