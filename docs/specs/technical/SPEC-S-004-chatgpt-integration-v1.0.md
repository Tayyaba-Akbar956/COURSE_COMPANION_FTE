# SPEC-S-004-chatgpt-integration-v1.0

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

This spec defines how the ChatGPT App integrates with our backend, including API calls, authentication, and data flow.

## 2. Architecture

```
┌─────────────┐
│   Student   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  ChatGPT    │
│     App     │
└──────┬──────┘
       │ Calls our backend APIs
       │ via Actions
       ▼
┌─────────────┐
│   Our       │
│  Backend    │
│  (FastAPI)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Supabase   │
│  Database   │
└─────────────┘
```

## 3. ChatGPT App Manifest

```yaml
# chatgpt-app/manifest.yaml

schema_version: v1
name: "GenAI Tutor"
description: "Your 24/7 AI tutor for Generative AI Fundamentals course"
auth:
  type: oauth
  authorization_url: https://your-project.supabase.co/auth/v1/authorize
  token_url: https://your-project.supabase.co/auth/v1/token
  scope: "read write"
api:
  type: openapi
  url: https://your-backend.railway.app/openapi.json
  has_user_authentication: true
logo_url: https://cdn.example.com/logo.png
contact_email: support@example.com
```

## 4. AI Instructions

```markdown
# chatgpt-app/instructions.md

You are the GenAI Tutor, an AI-powered educational assistant for the "Generative AI Fundamentals" course.

## Your Role
- Help students learn generative AI concepts
- Explain content from the course at appropriate levels
- Guide students through quizzes
- Track and celebrate progress
- Answer questions using ONLY course content

## How to Use the Backend APIs

### 1. When Student Asks About a Concept

**Example:** "What is a transformer?"

**Your Action:**
1. Call `GET /api/v1/search?q=transformer` to find relevant content
2. Use the returned content to formulate your explanation
3. Always cite the chapter: "According to Chapter 6..."
4. If no results: "That topic isn't covered in this course yet"

**DO NOT:**
- Make up information not in the course
- Use your general knowledge instead of course content
- Provide answers without checking the backend first

### 2. When Student Wants to Read a Chapter

**Example:** "I want to read Chapter 1"

**Your Action:**
1. Call `GET /api/v1/chapters/1` to get chapter content
2. Present the content in a readable format
3. Offer to explain difficult concepts
4. Suggest taking the quiz after reading

### 3. When Student Wants to Take a Quiz

**Example:** "Quiz me on Chapter 1"

**Your Action:**
1. Call `GET /api/v1/chapters/1/quiz` to get quiz questions
2. Present questions one at a time
3. Wait for student's answer
4. Call `POST /api/v1/quizzes/{id}/submit` to grade
5. Present results with encouragement

### 4. When Student Asks About Progress

**Example:** "How am I doing?"

**Your Action:**
1. Call `GET /api/v1/users/{user_id}/progress`
2. Present progress in an encouraging way
3. Highlight achievements and streaks
4. Suggest next steps

## Tone and Style
- Friendly and encouraging
- Adapt complexity to student's level
- Celebrate achievements enthusiastically
- Be patient with struggles
- Never condescending

## Grounding Rules
- ALWAYS search backend before answering content questions
- Cite chapter sources
- Say "I don't know" if content not found
- Never hallucinate information
```

## 5. API Action Examples

### 5.1 Search for Content

```json
{
  "action": "search_content",
  "parameters": {
    "query": "attention mechanism",
    "limit": 5
  },
  "response_handler": "format_search_results"
}
```

**Response Handler:**
```javascript
function format_search_results(results) {
  if (results.length === 0) {
    return "I couldn't find information about that in the course content.";
  }
  
  let response = "Based on the course content:\n\n";
  results.forEach((result, i) => {
    response += `From Chapter ${result.chapter_title}:\n`;
    response += `${result.excerpt}\n\n`;
  });
  
  return response;
}
```

### 5.2 Get Chapter Content

```json
{
  "action": "get_chapter",
  "parameters": {
    "chapter_id": 1
  },
  "response_handler": "format_chapter"
}
```

**Response Handler:**
```javascript
function format_chapter(chapter) {
  let response = `# ${chapter.title}\n\n`;
  response += `${chapter.content}\n\n`;
  
  if (chapter.code_examples.length > 0) {
    response += "## Code Example\n\n";
    chapter.code_examples.forEach(example => {
      response += `\`\`\`${example.language}\n${example.code}\n\`\`\`\n\n`;
    });
  }
  
  response += `\n\nWould you like me to explain any part, or shall we take the quiz?`;
  
  return response;
}
```

### 5.3 Submit Quiz

```json
{
  "action": "submit_quiz",
  "parameters": {
    "quiz_id": "quiz-123",
    "answers": [
      {"question_id": 1, "answer": "A"},
      {"question_id": 2, "answer": "B"}
    ]
  },
  "response_handler": "format_quiz_results"
}
```

**Response Handler:**
```javascript
function format_quiz_results(result) {
  let response = `## Quiz Complete!\n\n`;
  response += `**Score: ${result.score}%**\n\n`;
  
  if (result.passed) {
    response += `🎉 Congratulations! You passed!\n\n`;
  } else {
    response += `Keep studying! You can retake this quiz.\n\n`;
  }
  
  response += `### Review:\n\n`;
  result.answers.forEach((answer, i) => {
    response += `Q${i+1}: ${answer.is_correct ? '✅' : '❌'} `;
    response += `${answer.explanation}\n\n`;
  });
  
  return response;
}
```

## 6. Authentication Flow

```
1. User opens ChatGPT
2. ChatGPT detects GenAI Tutor app
3. User clicks "Connect"
4. Redirect to Supabase Auth
5. User logs in (magic link or OAuth)
6. Supabase returns JWT token
7. ChatGPT stores token
8. All API calls include token in Authorization header
```

**Token Usage:**
```javascript
// Every API call includes:
headers: {
  'Authorization': `Bearer ${user_jwt_token}`
}
```

## 7. Error Handling in ChatGPT

```javascript
// chatgpt-app/error-handler.js

async function handleApiError(error) {
  if (error.status === 401) {
    return "Please reconnect your account to continue.";
  }
  
  if (error.status === 403) {
    return "This content requires a premium subscription. Would you like to upgrade?";
  }
  
  if (error.status === 404) {
    return "I couldn't find that. Let me search for something else.";
  }
  
  if (error.status === 429) {
    return "I'm getting too many requests. Please wait a moment and try again.";
  }
  
  if (error.status >= 500) {
    return "I'm having technical difficulties. Please try again in a moment.";
  }
  
  return "I encountered an error. Let's try something else.";
}
```

## 8. Conversation Context

```javascript
// Maintain conversation context
const conversationState = {
  currentChapter: null,
  lastSearchedTopic: null,
  quizInProgress: false,
  quizId: null,
  answersSoFar: [],
  userLevel: 'intermediate', // detected from conversation
  recentAchievements: [],
};

// Update context based on interactions
function updateContext(action, data) {
  if (action === 'view_chapter') {
    conversationState.currentChapter = data.chapter_id;
  }
  
  if (action === 'start_quiz') {
    conversationState.quizInProgress = true;
    conversationState.quizId = data.quiz_id;
  }
  
  if (action === 'complete_quiz') {
    conversationState.quizInProgress = false;
    conversationState.recentAchievements.push(data.achievements);
  }
}
```

## 9. Testing Requirements

```typescript
// chatgpt-app/tests/integration.test.ts

test('search action returns course content', async () => {
  const result = await chatgptApp.action('search_content', {
    query: 'transformers'
  });
  
  expect(result).toContain('Chapter 6');
  expect(result).toContain('self-attention');
});

test('get_chapter action returns full chapter', async () => {
  const result = await chatgptApp.action('get_chapter', {
    chapter_id: 1
  });
  
  expect(result).toContain('# What is Generative AI?');
  expect(result).toContain('Code Example');
});

test('submit_quiz action grades correctly', async () => {
  const result = await chatgptApp.action('submit_quiz', {
    quiz_id: 'quiz-1',
    answers: [{question_id: 1, answer: 'A'}]
  });
  
  expect(result).toContain('Score:');
  expect(result).toContain('✅' || '❌');
});

test('handles 403 error gracefully', async () => {
  const result = await chatgptApp.action('get_chapter', {
    chapter_id: 5 // premium chapter for free user
  });
  
  expect(result).toContain('premium');
  expect(result).toContain('upgrade');
});
```

## 10. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** ChatGPT Integration Spec (SPEC-S-004-chatgpt-integration-v1.0)  
**Why:** Defines how ChatGPT App integrates with our backend  
**Files Affected:** `docs/specs/technical/SPEC-S-004-chatgpt-integration-v1.0.md`

**Do you approve?** (Yes/No/Modify)

---

## ✅ **ALL CRITICAL GAPS FIXED!**

### **Summary of New Specs:**

| Spec | Purpose | Status |
|------|---------|--------|
| **SPEC-S-001** | Pydantic Schemas (all request/response models) | ✅ Complete |
| **SPEC-S-002** | Error Handling (all edge cases) | ✅ Complete |
| **SPEC-S-003** | UI State Management (loading/error states) | ✅ Complete |
| **SPEC-S-004** | ChatGPT Integration (API actions, auth flow) | ✅ Complete |

### **Total Documents Created:** 33

**All critical gaps are now addressed. Ready to begin implementation!**

**Next Steps:**
1. Review and approve all 33 specs
2. Set up Supabase project
3. Start backend implementation (FastAPI + models + APIs)
4. Write tests alongside implementation

**Shall we proceed?**
