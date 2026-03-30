# SPEC-F-002-navigation-v1.0

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

This spec defines the Navigation feature that enables students to move sequentially through course chapters with next/previous links, module overview, and progress-based recommendations.

## 2. Functional Requirements

### FR-1: Sequential Navigation
- Students can navigate to next chapter from current chapter
- Students can navigate to previous chapter from current chapter
- First chapter has no previous link
- Last chapter has no next link

### FR-2: Module Navigation
- Students can view all chapters in current module
- Students can jump to any chapter within current module
- Module progress is visible (chapters completed / total)

### FR-3: Progress-Based Navigation
- Completed chapters are visually marked
- Current chapter is highlighted
- Locked chapters (premium, not accessible) are indicated
- Students can see which chapters are available to them

### FR-4: Quick Navigation
- Students can access table of contents (all chapters)
- Students can filter chapters by module
- Students can search chapters by title

## 3. Technical Requirements

### TR-1: Navigation Data
- Navigation data included in chapter response (next_id, prev_id)
- Module structure pre-calculated and cached
- User progress fetched from database

### TR-2: Performance
- Navigation data loads with chapter (no additional API calls)
- Table of contents loads in < 300ms
- Progress indicators update in real-time

### TR-3: Access Control
- Navigation respects user's access level
- Locked chapters visible but inaccessible to free users
- Clear visual distinction between free and premium chapters

### TR-4: State Management
- Current chapter state maintained during navigation
- Progress updates after chapter completion
- Navigation history tracked (for back button)

## 4. API Contract

### GET /api/v1/chapters/{chapter_id}/next

**Description:** Get next chapter in sequence

**Request:**
```http
GET /api/v1/chapters/1/next
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "next_chapter": {
    "id": 2,
    "title": "Evolution of AI: From Discriminative to Generative",
    "chapter_number": 2,
    "module": "Module 1",
    "is_free": true,
    "is_completed": false,
    "estimated_minutes": 20
  }
}
```

**Response (204 No Content):**
```
// No next chapter (current chapter is the last one)
```

**Response (403 Forbidden):**
```json
{
  "error": "access_denied",
  "message": "Next chapter requires premium access",
  "next_chapter_id": 5,
  "is_free": false,
  "upgrade_url": "/pricing"
}
```

### GET /api/v1/chapters/{chapter_id}/previous

**Description:** Get previous chapter in sequence

**Request:**
```http
GET /api/v1/chapters/5/previous
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "previous_chapter": {
    "id": 4,
    "title": "Applications and Use Cases",
    "chapter_number": 4,
    "module": "Module 1",
    "is_free": true,
    "is_completed": true,
    "estimated_minutes": 18
  }
}
```

**Response (204 No Content):**
```
// No previous chapter (current chapter is the first one)
```

### GET /api/v1/modules/{module_id}

**Description:** Get all chapters in a module

**Request:**
```http
GET /api/v1/modules/1
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "module": {
    "id": 1,
    "title": "Introduction to Generative AI",
    "description": "Foundational concepts in generative AI",
    "order": 1,
    "total_chapters": 4,
    "completed_chapters": 2,
    "completion_percentage": 50,
    "chapters": [
      {
        "id": 1,
        "title": "What is Generative AI?",
        "chapter_number": 1,
        "is_free": true,
        "is_completed": true,
        "estimated_minutes": 15,
        "quiz_completed": true,
        "quiz_score": 100
      },
      {
        "id": 2,
        "title": "Evolution of AI: From Discriminative to Generative",
        "chapter_number": 2,
        "is_free": true,
        "is_completed": true,
        "estimated_minutes": 20,
        "quiz_completed": true,
        "quiz_score": 80
      },
      {
        "id": 3,
        "title": "Key Concepts and Terminology",
        "chapter_number": 3,
        "is_free": true,
        "is_completed": false,
        "estimated_minutes": 25,
        "quiz_completed": false,
        "quiz_score": null
      },
      {
        "id": 4,
        "title": "Applications and Use Cases",
        "chapter_number": 4,
        "is_free": true,
        "is_completed": false,
        "estimated_minutes": 18,
        "quiz_completed": false,
        "quiz_score": null
      }
    ]
  }
}
```

### GET /api/v1/navigation

**Description:** Get complete navigation structure (table of contents)

**Request:**
```http
GET /api/v1/navigation
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "course": {
    "title": "Generative AI Fundamentals",
    "total_chapters": 24,
    "completed_chapters": 5,
    "overall_completion": 20.8
  },
  "user_access": {
    "is_premium": false,
    "accessible_chapters": [1, 2, 3, 4]
  },
  "modules": [
    {
      "id": 1,
      "title": "Introduction to Generative AI",
      "order": 1,
      "total_chapters": 4,
      "completed_chapters": 3,
      "chapters": [
        {
          "id": 1,
          "title": "What is Generative AI?",
          "chapter_number": 1,
          "is_free": true,
          "is_completed": true,
          "is_current": false,
          "is_locked": false
        },
        {
          "id": 2,
          "title": "Evolution of AI...",
          "chapter_number": 2,
          "is_free": true,
          "is_completed": true,
          "is_current": false,
          "is_locked": false
        },
        {
          "id": 3,
          "title": "Key Concepts...",
          "chapter_number": 3,
          "is_free": true,
          "is_completed": false,
          "is_current": true,
          "is_locked": false
        },
        {
          "id": 4,
          "title": "Applications...",
          "chapter_number": 4,
          "is_free": true,
          "is_completed": false,
          "is_current": false,
          "is_locked": false
        }
      ]
    },
    {
      "id": 2,
      "title": "Understanding Large Language Models",
      "order": 2,
      "total_chapters": 4,
      "completed_chapters": 0,
      "chapters": [
        {
          "id": 5,
          "title": "What are LLMs?",
          "chapter_number": 5,
          "is_free": false,
          "is_completed": false,
          "is_current": false,
          "is_locked": true
        },
        // ... more chapters
      ]
    }
    // ... more modules
  ],
  "navigation_metadata": {
    "current_chapter_id": 3,
    "next_available_chapter_id": 3,
    "last_accessed": "2026-03-29T10:30:00Z"
  }
}
```

### GET /api/v1/navigation/recommendations

**Description:** Get recommended next chapter based on progress

**Request:**
```http
GET /api/v1/navigation/recommendations
Authorization: Bearer {user_token}
```

**Response (200 OK):**
```json
{
  "recommendation": {
    "type": "continue_learning",
    "chapter_id": 3,
    "chapter_title": "Key Concepts and Terminology",
    "reason": "This is your next incomplete chapter",
    "module": "Module 1",
    "is_free": true,
    "estimated_minutes": 25
  },
  "alternatives": [
    {
      "chapter_id": 4,
      "chapter_title": "Applications and Use Cases",
      "reason": "Complete Module 1",
      "is_free": true
    },
    {
      "chapter_id": 1,
      "chapter_title": "What is Generative AI?",
      "reason": "Review for better understanding",
      "is_free": true,
      "quiz_score": 100
    }
  ]
}
```

**Response (Premium User):**
```json
{
  "recommendation": {
    "type": "continue_learning",
    "chapter_id": 10,
    "chapter_title": "Advanced Prompting Strategies",
    "reason": "Continue your learning path",
    "module": "Module 3",
    "is_free": true,
    "estimated_minutes": 30
  }
}
```

## 5. User Stories

### US-1: Student Continuing from Last Position
**As a** student  
**I want** to know which chapter to continue with  
**So that** I can resume learning where I left off

**Acceptance Criteria:**
- [ ] Current chapter is clearly marked
- [ ] Recommendation API returns next incomplete chapter
- [ ] Can navigate directly to recommended chapter

### US-2: Student Moving Sequentially
**As a** student reading Chapter 3  
**I want** to easily go to Chapter 4  
**So that** I can follow the course in order

**Acceptance Criteria:**
- [ ] Next chapter link available in chapter view
- [ ] Next chapter endpoint returns chapter 4
- [ ] Navigation is instant (no page reload)

### US-3: Student Reviewing Previous Content
**As a** student reading Chapter 5  
**I want** to go back to Chapter 4  
**So that** I can review a concept I forgot

**Acceptance Criteria:**
- [ ] Previous chapter link available
- [ ] Previous chapter endpoint returns chapter 4
- [ ] Can navigate back multiple chapters

### US-4: Free User Seeing Premium Content
**As a** free user  
**I want** to see what premium content exists  
**So that** I can decide whether to upgrade

**Acceptance Criteria:**
- [ ] Premium chapters visible in navigation
- [ ] Premium chapters marked as locked
- [ ] Clear indication of what requires upgrade
- [ ] Upgrade option easily accessible

### US-5: Student Viewing Module Progress
**As a** student  
**I want** to see my progress in current module  
**So that** I know how much is left

**Acceptance Criteria:**
- [ ] Module view shows completed/total chapters
- [ ] Completion percentage displayed
- [ ] Visual progress indicator
- [ ] Quiz completion status shown

### US-6: Student Browsing Table of Contents
**As a** student  
**I want** to see all chapters at once  
**So that** I can understand course structure

**Acceptance Criteria:**
- [ ] Navigation endpoint returns all chapters
- [ ] Chapters grouped by module
- [ ] Completion status visible for each
- [ ] Can filter by module

## 6. Acceptance Criteria

### Functional Tests
- [ ] Next navigation returns correct chapter
- [ ] Previous navigation returns correct chapter
- [ ] First chapter has no previous
- [ ] Last chapter has no next
- [ ] Module view shows all chapters in module
- [ ] Navigation respects access control
- [ ] Recommendations are progress-based
- [ ] Completed chapters marked correctly
- [ ] Current chapter highlighted
- [ ] Locked chapters indicated clearly

### Non-Functional Tests
- [ ] Navigation data loads in < 300ms
- [ ] No additional API calls needed for basic navigation
- [ ] Progress updates reflect immediately
- [ ] Navigation works on mobile devices
- [ ] Smooth transitions between chapters

## 7. Dependencies

### Internal Dependencies
- SPEC-F-001-content-delivery-v1.0.md (chapter access)
- SPEC-F-005-progress-tracking-v1.0.md (completion status)
- SPEC-T-001-database-schema-v1.0.md (chapter ordering)

### External Dependencies
- Supabase (PostgreSQL for chapter data)
- User progress tracking in database

## 8. Out of Scope

This spec does NOT cover:
- Adaptive learning paths (Phase 2 feature)
- AI-generated recommendations (Phase 2)
- Social navigation (seeing what others are studying)
- Bookmarks or favorites (Phase 3)
- Custom learning paths (Phase 3)
- Offline navigation (requires internet)

## 9. Testing Requirements

### Test Scenarios

#### Test 1: Next Chapter Navigation
```python
def test_navigation_next_returns_correct_chapter():
    """Next navigation from chapter 1 should return chapter 2"""
    # Arrange: User on chapter 1
    # Act: GET /api/v1/chapters/1/next
    # Assert: Returns chapter 2, correct metadata
```

#### Test 2: Previous Chapter Navigation
```python
def test_navigation_previous_returns_correct_chapter():
    """Previous navigation from chapter 5 should return chapter 4"""
    # Arrange: User on chapter 5
    # Act: GET /api/v1/chapters/5/previous
    # Assert: Returns chapter 4, correct metadata
```

#### Test 3: First Chapter Has No Previous
```python
def test_navigation_first_chapter_no_previous():
    """First chapter should return 204 for previous endpoint"""
    # Arrange: User on chapter 1
    # Act: GET /api/v1/chapters/1/previous
    # Assert: 204 No Content
```

#### Test 4: Last Chapter Has No Next
```python
def test_navigation_last_chapter_no_next():
    """Last chapter should return 204 for next endpoint"""
    # Arrange: User on chapter 24
    # Act: GET /api/v1/chapters/24/next
    # Assert: 204 No Content
```

#### Test 5: Free User Navigation to Premium Chapter
```python
def test_navigation_free_user_premium_next():
    """Free user should get 403 when next chapter is premium"""
    # Arrange: Free user on chapter 4, next is chapter 5 (premium)
    # Act: GET /api/v1/chapters/4/next
    # Assert: 403 Forbidden, upgrade message
```

#### Test 6: Module View Returns All Chapters
```python
def test_navigation_module_view_returns_all_chapters():
    """Module endpoint should return all chapters in module"""
    # Arrange: Module 1 has 4 chapters
    # Act: GET /api/v1/modules/1
    # Assert: Returns 4 chapters, correct order, completion status
```

#### Test 7: Navigation Includes Progress
```python
def test_navigation_includes_progress_data():
    """Navigation should include completion status"""
    # Arrange: User has completed chapters 1-3
    # Act: GET /api/v1/navigation
    # Assert: Chapters 1-3 marked is_completed=true, chapter 4 is_current
```

#### Test 8: Recommendations Based on Progress
```python
def test_navigation_recommendations_based_on_progress():
    """Recommendations should suggest next incomplete chapter"""
    # Arrange: User completed chapters 1-2, current is 3
    # Act: GET /api/v1/navigation/recommendations
    # Assert: Recommends chapter 3, reason is "next incomplete"
```

### Coverage Requirements
- Minimum 90% code coverage
- All navigation endpoints tested
- Access control scenarios tested
- Edge cases (first/last chapter) tested

## 10. Open Questions

1. **Skip Navigation:** Should students be able to skip chapters they've completed?
2. **Prerequisite Enforcement:** Should we require quiz completion before moving to next chapter?
3. **Multiple Paths:** Should we support alternative chapter orderings for different learning styles?
4. **Quick Jump:** Should we allow jumping to any chapter (within access level) or enforce sequential?

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Navigation Spec (SPEC-F-002-navigation-v1.0)  
**Why:** Defines how students navigate through course chapters (core Phase 1 feature)  
**Files Affected:** 
- `docs/specs/functional/SPEC-F-002-navigation-v1.0.md`

**Key Decisions:**
- Next/previous endpoints for sequential navigation
- Module view for browsing chapters within module
- Complete navigation endpoint for table of contents
- Recommendations based on progress (simple, rule-based)
- Locked chapters visible but inaccessible to free users
- Navigation data included in chapter responses

**Do you approve this spec?** (Yes/No/Modify)

If approved, next step is to:
1. Create test file: `backend/tests/test_navigation_api.py`
2. Write failing tests
3. Implement minimum code to pass
4. Repeat until all tests pass
