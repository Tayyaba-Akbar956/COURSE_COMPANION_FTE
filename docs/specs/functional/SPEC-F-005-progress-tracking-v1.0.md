# SPEC-F-005-progress-tracking-v1.0

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

This spec defines the Progress Tracking feature that enables students to monitor their learning journey through the course, including chapter completion, quiz scores, streaks, achievements, and time spent learning.

## 2. Functional Requirements

### FR-1: Chapter Completion Tracking
- Track which chapters student has completed
- Mark chapter as complete when student finishes reading
- Track percentage of chapter read (optional, Phase 2)
- Track time spent on each chapter
- Track last accessed timestamp

### FR-2: Quiz Performance Tracking
- Track all quiz attempts per chapter
- Store score for each attempt
- Track best score, latest score, average score
- Track time taken for each quiz
- Track questions answered correctly/incorrectly (aggregate)

### FR-3: Streak Tracking
- Track consecutive days of learning activity
- Define "activity" as: completing a chapter OR taking a quiz OR spending 5+ minutes
- Reset streak if day missed (midnight UTC)
- Track longest streak ever
- Track current streak
- Display streak count prominently

### FR-4: Achievement System
- Define achievement badges for milestones
- Award achievements automatically when criteria met
- Track achievement unlock timestamps
- Display all earned achievements
- Show progress toward locked achievements

### FR-5: Course Progress Overview
- Show overall completion percentage (chapters completed / total)
- Show module-by-module progress
- Show estimated time to completion (based on pace)
- Show time spent learning (total minutes)
- Show activity history (last 7 days, last 30 days)

### FR-6: Progress Visualization
- Visual progress bars for modules
- Completion checkmarks for chapters
- Quiz score indicators (color-coded: green >80%, yellow 60-79%, red <60%)
- Streak flame icon with count
- Achievement badges grid

### FR-7: Progress Persistence
- Progress saved automatically
- Progress synced across devices
- Progress exportable (JSON download)
- Progress retained indefinitely (no expiration)

## 3. Technical Requirements

### TR-1: Data Storage
- Progress stored in PostgreSQL database (Supabase)
- One row per user in progress table
- Chapter completion stored as array or junction table
- Quiz history stored as separate table
- Achievements stored as junction table (user_id, achievement_id, unlocked_at)

### TR-2: Real-Time Updates
- Progress updated immediately after chapter completion
- Progress updated immediately after quiz submission
- Streak updated on first activity of day
- WebSocket or polling for live updates (Phase 2)

### TR-3: Performance
- Progress endpoint response time < 200ms (p95)
- Streak calculation optimized (cache current streak)
- Achievement checks run asynchronously (don't block user actions)
- Progress data cached for 5 minutes (reduce database reads)

### TR-4: Data Integrity
- Progress updates are idempotent (safe to retry)
- Quiz scores immutable once recorded (can add, not modify)
- Streak calculation deterministic (same result every time)
- Audit trail for all progress changes

### TR-5: Privacy
- Progress data private to user (not visible to others)
- User can request progress data export (GDPR compliance)
- User can request account deletion (progress deleted with account)
- No progress data shared with third parties

## 4. API Contract

### GET /api/v1/users/{user_id}/progress

**Description:** Get comprehensive progress for a user

**Request:**
```http
GET /api/v1/users/user123/progress
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "user_id": "user123",
  "course": {
    "title": "Generative AI Fundamentals",
    "total_chapters": 24,
    "total_modules": 6
  },
  "overall_progress": {
    "chapters_completed": 5,
    "total_chapters": 24,
    "completion_percentage": 20.8,
    "quizzes_completed": 4,
    "total_quizzes": 24,
    "average_quiz_score": 87.5,
    "time_spent_minutes": 320,
    "first_activity": "2026-03-15T08:00:00Z",
    "last_activity": "2026-03-29T10:30:00Z"
  },
  "streak": {
    "current_streak": 5,
    "longest_streak": 7,
    "streak_start_date": "2026-03-25",
    "last_activity_date": "2026-03-29",
    "streak_active": true
  },
  "module_progress": [
    {
      "module_id": 1,
      "module_title": "Introduction to Generative AI",
      "chapters_completed": 3,
      "total_chapters": 4,
      "completion_percentage": 75,
      "quizzes_passed": 3,
      "average_quiz_score": 90,
      "chapters": [
        {"chapter_id": 1, "completed": true, "quiz_score": 100},
        {"chapter_id": 2, "completed": true, "quiz_score": 80},
        {"chapter_id": 3, "completed": true, "quiz_score": 90},
        {"chapter_id": 4, "completed": false, "quiz_score": null}
      ]
    },
    {
      "module_id": 2,
      "module_title": "Understanding Large Language Models",
      "chapters_completed": 2,
      "total_chapters": 4,
      "completion_percentage": 50,
      "quizzes_passed": 2,
      "average_quiz_score": 85,
      "chapters": [
        {"chapter_id": 5, "completed": true, "quiz_score": 80},
        {"chapter_id": 6, "completed": true, "quiz_score": 90},
        {"chapter_id": 7, "completed": false, "quiz_score": null},
        {"chapter_id": 8, "completed": false, "quiz_score": null}
      ]
    }
    // ... more modules
  ],
  "achievements": {
    "earned": [
      {
        "achievement_id": "first_chapter",
        "name": "First Steps",
        "description": "Complete your first chapter",
        "icon": "🏅",
        "unlocked_at": "2026-03-15T08:30:00Z"
      },
      {
        "achievement_id": "quiz_perfect",
        "name": "Perfectionist",
        "description": "Get 100% on any quiz",
        "icon": "🎯",
        "unlocked_at": "2026-03-15T09:00:00Z"
      },
      {
        "achievement_id": "streak_5",
        "name": "Consistent Learner",
        "description": "5-day learning streak",
        "icon": "🔥",
        "unlocked_at": "2026-03-29T10:30:00Z"
      }
    ],
    "locked": [
      {
        "achievement_id": "streak_10",
        "name": "Dedicated Scholar",
        "description": "10-day learning streak",
        "icon": "⚡",
        "progress": 5,
        "target": 10,
        "progress_percentage": 50
      },
      {
        "achievement_id": "course_complete",
        "name": "Graduate",
        "description": "Complete the entire course",
        "icon": "🎓",
        "progress": 5,
        "target": 24,
        "progress_percentage": 20.8
      }
    ]
  },
  "activity_history": {
    "last_7_days": [
      {"date": "2026-03-23", "chapters": 1, "quizzes": 1, "minutes": 45},
      {"date": "2026-03-24", "chapters": 1, "quizzes": 1, "minutes": 50},
      {"date": "2026-03-25", "chapters": 0, "quizzes": 1, "minutes": 15},
      {"date": "2026-03-26", "chapters": 1, "quizzes": 0, "minutes": 30},
      {"date": "2026-03-27", "chapters": 0, "quizzes": 1, "minutes": 20},
      {"date": "2026-03-28", "chapters": 1, "quizzes": 1, "minutes": 55},
      {"date": "2026-03-29", "chapters": 0, "quizzes": 0, "minutes": 10}
    ],
    "total_days_active": 45,
    "average_minutes_per_day": 35
  },
  "next_milestones": [
    {
      "type": "chapter_completion",
      "title": "Complete Chapter 7",
      "description": "You're 1 chapter away from completing Module 2",
      "progress": 3,
      "target": 4
    },
    {
      "type": "streak",
      "title": "Maintain your streak",
      "description": "Come back tomorrow to keep your 5-day streak alive!",
      "progress": 5,
      "target": 6
    }
  ]
}
```

### PUT /api/v1/users/{user_id}/progress

**Description:** Update user progress (after chapter completion or quiz submission)

**Request:**
```http
PUT /api/v1/users/user123/progress
Authorization: Bearer {user_token}
Content-Type: application/json

{
  "chapter_id": 7,
  "action": "complete",
  "quiz_score": null,
  "time_spent_seconds": 1200,
  "completed_at": "2026-03-29T11:00:00Z"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "progress_updated": {
    "chapter_id": 7,
    "completed": true,
    "completed_at": "2026-03-29T11:00:00Z"
  },
  "achievements_unlocked": [
    {
      "achievement_id": "module_2_complete",
      "name": "Module 2 Master",
      "description": "Complete all chapters in Module 2",
      "icon": "🎯"
    }
  ],
  "streak_updated": {
    "current_streak": 5,
    "streak_maintained": true
  },
  "new_overall_progress": {
    "chapters_completed": 6,
    "completion_percentage": 25.0
  }
}
```

### POST /api/v1/users/{user_id}/progress/quiz

**Description:** Record quiz completion

**Request:**
```http
POST /api/v1/users/user123/progress/quiz
Authorization: Bearer {user_token}
Content-Type: application/json

{
  "chapter_id": 7,
  "quiz_id": "quiz-session-xyz",
  "score": 80,
  "passed": true,
  "time_taken_seconds": 180,
  "attempt_number": 1
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "quiz_recorded": {
    "chapter_id": 7,
    "score": 80,
    "passed": true,
    "attempt_number": 1
  },
  "achievements_unlocked": [],
  "new_average_score": 86.4
}
```

### GET /api/v1/users/{user_id}/progress/export

**Description:** Export all progress data (GDPR compliance)

**Request:**
```http
GET /api/v1/users/user123/progress/export
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "export_generated_at": "2026-03-29T12:00:00Z",
  "user_id": "user123",
  "data": {
    // Complete progress data in structured format
  },
  "download_url": "https://r2.example.com/exports/user123-progress-2026-03-29.json",
  "expires_at": "2026-04-05T12:00:00Z"
}
```

## 5. User Stories

### US-1: Student Viewing Overall Progress
**As a** student  
**I want** to see my overall course progress  
**So that** I know how far I've come

**Acceptance Criteria:**
- [ ] Completion percentage displayed (chapters completed / total)
- [ ] Visual progress bar
- [ ] Time spent learning shown
- [ ] Last activity date shown

### US-2: Student Tracking Daily Streak
**As a** student  
**I want** to see my current learning streak  
**So that** I'm motivated to continue daily

**Acceptance Criteria:**
- [ ] Current streak count visible
- [ ] Longest streak shown for comparison
- [ ] Streak flame icon or visual indicator
- [ ] Clear when streak is active/expired

### US-3: Student Earning Achievements
**As a** student  
**I want** to earn badges for milestones  
**So that** I feel accomplished

**Acceptance Criteria:**
- [ ] Achievements unlock automatically
- [ ] Notification when achievement earned
- [ ] Achievement grid shows all earned badges
- [ ] Locked achievements show progress toward unlock

### US-4: Student Viewing Module Progress
**As a** student  
**I want** to see progress per module  
**So that** I know which modules I've completed

**Acceptance Criteria:**
- [ ] Each module shows completion percentage
- [ ] Chapters within module show checkmarks if completed
- [ ] Quiz scores visible per chapter
- [ ] Module progress color-coded

### US-5: Student Viewing Activity History
**As a** student  
**I want** to see my learning activity over time  
**So that** I can track my consistency

**Acceptance Criteria:**
- [ ] Last 7 days activity shown
- [ ] Each day shows chapters, quizzes, minutes
- [ ] Visual chart or calendar view
- [ ] Total days active shown

### US-6: Student Exporting Progress Data
**As a** student  
**I want** to download my progress data  
**So that** I have a record of my learning

**Acceptance Criteria:**
- [ ] Export button available
- [ ] Generates JSON file with all progress
- [ ] Download link provided
- [ ] Link expires after 7 days

## 6. Acceptance Criteria

### Functional Tests
- [ ] Chapter completion tracked correctly
- [ ] Quiz scores recorded accurately
- [ ] Streak calculated correctly (consecutive days)
- [ ] Achievements unlock at correct thresholds
- [ ] Module progress aggregated correctly
- [ ] Activity history tracked accurately
- [ ] Progress export generates valid JSON
- [ ] Progress updates in real-time

### Non-Functional Tests
- [ ] Progress endpoint responds in < 200ms
- [ ] Streak calculation optimized (cached)
- [ ] Progress data persisted reliably
- [ ] Progress synced across devices
- [ ] Export generation doesn't block API
- [ ] Data privacy maintained (user can only access own progress)

## 7. Dependencies

### Internal Dependencies
- SPEC-F-001-content-delivery-v1.0.md (chapter access tracking)
- SPEC-F-004-rule-based-quizzes-v1.0.md (quiz score tracking)
- SPEC-T-001-database-schema-v1.0.md (progress data storage)

### External Dependencies
- Supabase PostgreSQL (progress storage)
- Cloudflare R2 (export file storage)

## 8. Out of Scope

This spec does NOT cover:
- Social progress sharing (seeing other students' progress)
- Leaderboards or rankings (Phase 3)
- Adaptive learning recommendations based on progress (Phase 2)
- Progress certificates (Phase 3)
- Progress-based content unlocking (all content available, just gated by premium)
- Learning analytics dashboard for instructors (Phase 3)
- Progress predictions using ML (Phase 2 hybrid)

## 9. Testing Requirements

### Test Scenarios

#### Test 1: Chapter Completion Tracked
```python
def test_progress_chapter_completion_tracked():
    """Chapter completion should be recorded correctly"""
    # Arrange: User completes chapter 5
    # Act: PUT /api/v1/users/user123/progress with chapter_id=5
    # Assert: Chapter marked completed, timestamp recorded, progress percentage updated
```

#### Test 2: Quiz Score Recorded
```python
def test_progress_quiz_score_recorded():
    """Quiz score should be recorded correctly"""
    # Arrange: User scores 80% on chapter 5 quiz
    # Act: POST /api/v1/users/user123/progress/quiz
    # Assert: Score recorded, average updated, quiz history includes attempt
```

#### Test 3: Streak Calculated Correctly
```python
def test_progress_streak_calculated_correctly():
    """Streak should count consecutive days of activity"""
    # Arrange: User active for 5 consecutive days
    # Act: GET /api/v1/users/user123/progress
    # Assert: current_streak=5, streak_active=true
```

#### Test 4: Streak Resets After Missed Day
```python
def test_progress_streak_resets_after_missed_day():
    """Streak should reset if day is missed"""
    # Arrange: User has 5-day streak, skips a day
    # Act: Activity recorded on day 7 (day 6 missed)
    # Assert: current_streak=1, longest_streak=5
```

#### Test 5: Achievement Unlocks Automatically
```python
def test_progress_achievement_unlocks_automatically():
    """Achievement should unlock when criteria met"""
    # Arrange: User completes first chapter
    # Act: PUT /api/v1/users/user123/progress
    # Assert: first_chapter achievement unlocked, unlocked_at timestamp set
```

#### Test 6: Module Progress Aggregated
```python
def test_progress_module_progress_aggregated():
    """Module progress should show all chapters with completion status"""
    # Arrange: User completed 3 of 4 chapters in Module 1
    # Act: GET /api/v1/users/user123/progress
    # Assert: module_progress[0].completion_percentage=75, chapters show correct status
```

#### Test 7: Activity History Tracked
```python
def test_progress_activity_history_tracked():
    """Daily activity should be tracked accurately"""
    # Arrange: User completes 2 chapters and 1 quiz today
    # Act: GET /api/v1/users/user123/progress
    # Assert: activity_history.last_7_days includes today with correct counts
```

#### Test 8: Progress Export Generates File
```python
def test_progress_export_generates_file():
    """Export should generate downloadable JSON file"""
    # Arrange: User has progress data
    # Act: GET /api/v1/users/user123/progress/export
    # Assert: download_url provided, file contains all progress data, expires in 7 days
```

### Coverage Requirements
- Minimum 90% code coverage
- All progress endpoints tested
- Streak calculation edge cases tested (first day, missed day, longest streak)
- Achievement unlocking tested for all achievement types
- Privacy tests (user can only access own progress)

## 10. Open Questions

1. **Activity Definition:** What exactly counts as "activity" for streak? (chapter completion, quiz, time spent, any page view?)
2. **Streak Reset Time:** When does streak reset? (midnight UTC, midnight user's timezone, 24 hours from last activity?)
3. **Achievement Notifications:** Should achievements trigger email notifications or just in-app?
4. **Progress Rollback:** Should we allow undoing accidental chapter completions?
5. **Data Retention:** How long to keep progress data for inactive users? (indefinitely, 1 year, 2 years?)

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Progress Tracking Spec (SPEC-F-005-progress-tracking-v1.0)  
**Why:** Defines how student progress is tracked throughout the course (core Phase 1 feature)  
**Files Affected:** 
- `docs/specs/functional/SPEC-F-005-progress-tracking-v1.0.md`

**Key Decisions:**
- Track chapter completion, quiz scores, streaks, achievements
- Streak = consecutive days with any learning activity
- Achievements unlock automatically when criteria met
- Progress export available (GDPR compliance)
- Real-time progress updates
- Activity history tracked (last 7 days)
- Module-by-module progress breakdown

**Do you approve this spec?** (Yes/No/Modify)

If approved, next step is to:
1. Create test file: `backend/tests/test_progress_api.py`
2. Write failing tests
3. Implement minimum code to pass
4. Repeat until all tests pass

---

**Progress:** 5 of 6 Phase 1 feature specs complete! Remaining: SPEC-F-006 (Freemium Gate)
