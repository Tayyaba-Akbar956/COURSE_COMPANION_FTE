# ChatGPT App - GenAI Tutor

A ChatGPT App that provides 24/7 AI-powered tutoring for the Generative AI Fundamentals course.

## 🎯 Overview

This ChatGPT App integrates with the Course Companion backend to provide:
- **Concept Explanations** - Clear, course-based explanations
- **Interactive Quizzes** - Chapter-by-chapter knowledge checks
- **Progress Tracking** - Monitor completion and streaks
- **Personalized Guidance** - Adaptive teaching based on student needs

## 📁 Files

```
chatgpt-app/
├── manifest.yaml          # App configuration for ChatGPT
├── instructions.md        # AI tutor behavior specification
└── README.md             # This file
```

## 🔧 Setup

### 1. Configure Backend URL

Update `manifest.yaml` with your deployed backend URL:

```yaml
api:
  type: openapi
  url: https://your-backend.railway.app/openapi.json
```

### 2. Configure Supabase Auth

Update `manifest.yaml` with your Supabase project URL:

```yaml
auth:
  type: oauth
  authorization_url: https://your-project.supabase.co/auth/v1/authorize
  token_url: https://your-project.supabase.co/auth/v1/token
```

### 3. Add Logo (Optional)

Place your logo at a publicly accessible URL and update:

```yaml
logo_url: https://cdn.example.com/genai-tutor-logo.png
```

### 4. Deploy to ChatGPT

1. Go to [ChatGPT Developer Platform](https://platform.openai.com/)
2. Navigate to **Apps** → **Create New App**
3. Upload `manifest.yaml`
4. Configure authentication
5. Submit for review

## 🎓 How It Works

### Architecture

```
┌─────────────┐
│   Student   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  ChatGPT    │
│     App     │
│ (GenAI Tutor)│
└──────┬──────┘
       │ API Calls
       │ (via Actions)
       ▼
┌─────────────┐
│   Backend   │
│  (FastAPI)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Supabase   │
│  Database   │
└─────────────┘
```

### User Flow

1. **User starts conversation** with GenAI Tutor in ChatGPT
2. **ChatGPT authenticates** user via Supabase OAuth
3. **AI tutor calls backend APIs** to fetch content, quizzes, progress
4. **AI tutor presents information** in conversational format
5. **User interacts** naturally (asks questions, takes quizzes)
6. **Progress is saved** to database via backend

## 📡 API Integration

### Authentication

All API calls include the user's JWT token:

```http
Authorization: Bearer {user_token}
```

### Key Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/chapters` | GET | List all chapters |
| `/api/v1/chapters/{id}` | GET | Get chapter content |
| `/api/v1/chapters/{id}/quiz` | GET | Get quiz for chapter |
| `/api/v1/chapters/quizzes/{id}/submit` | POST | Submit quiz |
| `/api/v1/progress` | GET | Get user progress |
| `/api/v1/search?q=query` | GET | Search content |

## 🤖 AI Behavior

### Teaching Style

The AI tutor follows these principles:

- **Course-Based** - Uses ONLY course content, never makes things up
- **Citing Sources** - Always references chapter numbers
- **Encouraging** - Celebrates progress and motivates students
- **Adaptive** - Adjusts explanation depth based on student level
- **Interactive** - Asks questions, guides discovery

### Example Interactions

#### Concept Question

**User:** "What is a transformer?"

**AI:**
> "Great question! According to Chapter 6: Attention Mechanisms and Transformers, a transformer is a neural network architecture that uses self-attention to process sequences. Unlike RNNs, transformers can process all positions in parallel, making them much faster to train..."

#### Quiz Request

**User:** "Quiz me on Chapter 3"

**AI:**
> "Ready! Here's your first question:
> 
> **Question 1 of 5:**
> What does 'GAN' stand for?
> 
> A) Generative Adversarial Network
> B) General Artificial Network
> C) Gradient Ascent Network
> D) Graphical Analytics Network
> 
> What's your answer?"

#### Progress Check

**User:** "How am I doing?"

**AI:**
> "You're making excellent progress! 🎉
> 
> 📊 **Your Stats:**
> - Chapters completed: 8/24 (33%)
> - Current streak: 5 days 🔥
> - Quiz average: 92%
> 
> 🏆 **Latest Achievement:**
> - Fast Learner (completed 5 chapters in one week)
> 
> Keep up the great work! 💪"

## 🎯 Features

### 1. Concept Explanations

- Search course content for relevant information
- Explain in multiple ways if student doesn't understand
- Use analogies and examples from course
- Cite specific chapters

### 2. Chapter Navigation

- Help students access any chapter
- Check subscription tier (Free vs Premium)
- Present content in digestible sections
- Offer to start quiz after chapter

### 3. Interactive Quizzes

- Present questions one at a time
- Wait for student answers
- Grade and provide detailed explanations
- Track attempts and scores

### 4. Progress Tracking

- Show chapter completion
- Display daily streaks
- List unlocked achievements
- Provide motivational updates

### 5. Search & Discovery

- Find content by keyword
- Suggest related chapters
- Help students find what they need

## 🔐 Authentication

### OAuth Flow

1. User clicks GenAI Tutor in ChatGPT
2. ChatGPT redirects to Supabase auth
3. User logs in (magic link or OAuth)
4. Supabase returns JWT token to ChatGPT
5. ChatGPT includes token in all API calls

### Supported Auth Methods

- **Magic Links** (primary)
- **Google OAuth**
- **GitHub OAuth**
- **Email/Password** (fallback)

## 🎨 Customization

### Branding

Update these in `manifest.yaml`:

```yaml
name: "GenAI Tutor"
description: "Your 24/7 AI-powered tutor..."
logo_url: https://example.com/logo.png
contact_email: support@example.com
```

### Welcome Message

Update in `manifest.yaml`:

```yaml
welcome_message: |
  Hi! I'm your GenAI Tutor, here to help you master Generative AI Fundamentals. 🎓
  
  I can:
  • Explain course concepts in different ways
  • Guide you through chapter quizzes
  • Track your progress and celebrate wins
  
  What would you like to learn today?
```

### AI Personality

Edit `instructions.md` to customize:
- Teaching style
- Response tone
- Encouragement phrases
- Error handling

## 🧪 Testing

### Manual Testing Checklist

- [ ] User can authenticate
- [ ] AI can explain concepts from course
- [ ] AI cites chapter sources
- [ ] Quizzes work (questions, answers, grading)
- [ ] Progress tracking displays correctly
- [ ] Free/Premium tier gating works
- [ ] Error messages are user-friendly

### Test Scenarios

1. **New Free User**
   - Signs up
   - Accesses Chapter 1-4
   - Takes quizzes
   - Sees progress

2. **Premium User**
   - Upgrades subscription
   - Accesses all 24 chapters
   - Completes full course
   - Unlocks achievements

3. **Error Handling**
   - Backend unavailable
   - Invalid chapter ID
   - Expired token
   - Network timeout

## 🚀 Deployment

### Prerequisites

- Deployed backend (Railway)
- Supabase project configured
- ChatGPT Developer account

### Steps

1. **Update Configuration**
   - Backend URL in `manifest.yaml`
   - Supabase URLs in `manifest.yaml`
   - Logo and branding

2. **Submit to ChatGPT**
   - Upload manifest to ChatGPT platform
   - Configure OAuth
   - Submit for review

3. **Test in Production**
   - Install app in ChatGPT
   - Test all flows
   - Monitor logs

4. **Launch**
   - Publish app
   - Announce to students
   - Monitor usage

## 📊 Monitoring

### Metrics to Track

- Daily active users
- Chapters accessed
- Quizzes taken
- Average quiz scores
- Completion rates
- Streak lengths

### Logs

Monitor:
- API call frequency
- Error rates
- Authentication failures
- Response times

## 🆘 Troubleshooting

### Common Issues

**"Couldn't connect to backend"**
- Check backend is running
- Verify URL in manifest.yaml
- Check CORS settings

**"Authentication failed"**
- Verify Supabase configuration
- Check OAuth redirect URIs
- Ensure JWT tokens are valid

**"Content not found"**
- Check chapter IDs exist
- Verify search index is populated
- Ensure content is in database

## 📚 Related Documentation

- [Backend README](../backend/README.md)
- [API Documentation](../docs_external/API.md)
- [Architecture](../docs_external/ARCHITECTURE.md)
- [Phase 1 Spec](../docs/specs/functional/SPEC-F-000-phase-1-overview.md)

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-30 | Initial implementation |

## 📄 License

Open Source (as per course license)

---

**GenAI Tutor - Making Generative AI education accessible to everyone! 🚀**
