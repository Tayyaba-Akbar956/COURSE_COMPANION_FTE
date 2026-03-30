# Course Companion FTE - Generative AI Fundamentals

🎓 **A 24/7 AI-powered digital tutor for Generative AI Fundamentals**

## Overview

This project implements a **Digital Full-Time Equivalent (FTE) Educational Tutor** that:
- Works 168 hours/week (24/7)
- Provides 85-90% cost savings vs human tutors
- Scales from 10 to 100,000 users without linear cost increase
- Uses **Zero-Backend-LLM** architecture in Phase 1
- Adds selective **Hybrid Intelligence** in Phase 2
- Delivers full LMS experience in Phase 3

## Quick Links

- 📖 [Project Operating Manual (QWEN.md)](./QWEN.md)
- 📐 [Architecture Documentation](./docs/ARCHITECTURE.md)
- 📝 [API Documentation](./docs/API.md)
- 🚀 [Deployment Guide](./docs/DEPLOYMENT.md)
- 📊 [Cost Analysis](./docs/COST-ANALYSIS.md)

## Project Structure

```
course-companion-fte/
├── specs/           # Specifications (functional, technical, API)
├── skills/          # Agent skills (AI tutor behaviors)
├── backend/         # FastAPI backend
├── chatgpt-app/     # ChatGPT app (Phase 1 & 2)
├── web-app/         # Next.js web app (Phase 3)
├── content/         # Course content
├── docs/            # Documentation
├── decisions/       # Architecture Decision Records
├── logs/            # Conversation logs
└── approvals/       # Approval tracking
```

## Development Principles

1. **Spec-First:** Write complete specs BEFORE any code
2. **Test-Driven:** Write tests BEFORE implementation (90% coverage required)
3. **No Mocking:** Real database for all tests (SQLite in-memory)
4. **Document Everything:** Every decision, conversation, approval
5. **No Blind Decisions:** Explicit permission for EVERYTHING

## Tech Stack

### Backend (Phase 1, 2, 3)
- **Framework:** FastAPI (Python 3.12)
- **Database:** Supabase (PostgreSQL)
- **ORM:** SQLModel
- **Testing:** pytest (90% coverage required)
- **Hosting:** Railway

### ChatGPT App (Phase 1 & 2)
- **SDK:** OpenAI Apps SDK
- **Manifest:** YAML configuration

### Web App (Phase 3)
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Components:** shadcn/ui
- **Testing:** Playwright
- **Hosting:** Vercel

### Infrastructure
- **Database:** Supabase (Free tier)
- **Content Storage:** Cloudflare R2 (Free tier)
- **Auth:** Supabase Auth (Magic links, OAuth)

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 20+
- Docker (optional, for local development)
- Git

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Web App Setup (Phase 3)

```bash
cd web-app
npm install
npm run dev
```

## Phases

### Phase 1: Zero-Backend-LLM ChatGPT App
- ✅ Backend makes ZERO LLM calls
- ✅ ChatGPT handles all explanation/tutoring
- ✅ 6 required features implemented
- ✅ Freemium gate (Chapters 1-3 free)

### Phase 2: Hybrid Intelligence (Premium)
- ⏳ Selective backend LLM features
- ⏳ Maximum 2 hybrid features
- ⏳ Premium-gated, user-initiated
- ⏳ Cost tracking implemented

### Phase 3: Web App
- ⏳ Full Next.js LMS dashboard
- ⏳ All features consolidated
- ⏳ Progress visualizations
- ⏳ Admin features

## Required Features

| # | Feature | Description |
|---|---------|-------------|
| 1 | Content Delivery | Serve course chapters verbatim |
| 2 | Navigation | Next/previous chapter sequencing |
| 3 | Grounded Q&A | Answer from content only |
| 4 | Rule-Based Quizzes | Multiple-choice with answer keys |
| 5 | Progress Tracking | Completion, streaks, achievements |
| 6 | Freemium Gate | Free: Chapters 1-3, Premium: All |

## Testing

### Backend Tests
```bash
cd backend
pytest --cov=app --cov-report=html --cov-fail-under=90
```

### Frontend Tests (Phase 3)
```bash
cd web-app
npm run test
npm run test:e2e
```

## Code Quality

### Backend
```bash
ruff check backend
black --check backend
mypy backend
```

### Frontend
```bash
npm run lint
```

## Pre-commit Hooks

```bash
pre-commit install
pre-commit run --all-files
```

## Documentation

- **QWEN.md:** Complete operating manual
- **Specs:** All features have functional + technical + API specs
- **ADRs:** Architecture Decision Records in `decisions/`
- **Logs:** Conversation logs in `logs/`
- **Approvals:** Approval tracking in `approvals/`

## Hackathon Deliverables

- [ ] Source Code (GitHub repo)
- [ ] Architecture Diagram
- [ ] Spec Documents
- [ ] Cost Analysis
- [ ] Demo Video (5 min)
- [ ] API Documentation (OpenAPI)
- [ ] ChatGPT App Manifest
- [ ] SKILL.md files

## License

Open Source

## Contact

Project Manager: [User]  
AI Builder: Qwen Code

---

**Built with ❤️ for the Panaversity Agent Factory Hackathon IV**

*Last Updated: March 29, 2026*
