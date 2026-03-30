# QWEN.md - Project Operating Manual

**Project:** Course Companion FTE - Generative AI Fundamentals  
**Version:** 1.0.0  
**Created:** March 29, 2026  
**Last Updated:** March 29, 2026  
**Status:** Active Development

---

## **Table of Contents**

1. [Project Overview](#1-project-overview)
2. [Development Principles](#2-development-principles)
3. [Technology Stack](#3-technology-stack)
4. [Spec-Driven Development Process](#4-spec-driven-development-process)
5. [Test-Driven Development Process](#5-test-driven-development-process)
6. [Decision Documentation Process](#6-decision-documentation-process)
7. [Approval Workflow](#7-approval-workflow)
8. [File Structure](#8-file-structure)
9. [Communication Protocol](#9-communication-protocol)
10. [Quality Standards](#10-quality-standards)
11. [Security Guidelines](#11-security-guidelines)
12. [Deployment Strategy](#12-deployment-strategy)
13. [Monitoring & Maintenance](#13-monitoring--maintenance)
14. [Appendices](#14-appendices)

---

## **1. Project Overview**

### **1.1 What We're Building**

A **24/7 AI-powered digital tutor** for **Generative AI Fundamentals** that:
- Teaches 20-30 chapters of intermediate-level content
- Lives inside ChatGPT (Phase 1 & 2) AND as a standalone Web App (Phase 3)
- Uses Zero-Backend-LLM architecture in Phase 1 (no LLM calls in backend)
- Adds selective Hybrid intelligence in Phase 2 (premium features)
- Provides full LMS features in Phase 3

### **1.2 Course Details**

| Attribute | Value |
|-----------|-------|
| **Course Title** | Generative AI Fundamentals |
| **Target Audience** | Intermediate learners (know basic Python) |
| **Total Chapters** | 20-30 chapters |
| **Content Type** | Text + Code Examples + Diagrams + Images |
| **Content Creation** | AI-assisted generation (documented in specs) |
| **License** | Open Source |

### **1.3 Phase Strategy**

```
Phase 1 (Zero-Backend-LLM) → Test & Validate → Phase 2 (Hybrid Premium) → Test & Validate → Phase 3 (Web App)
```

**Phase 1:** ChatGPT App with deterministic backend (NO LLM calls)  
**Phase 2:** Add 3 hybrid features (Adaptive Path, LLM Assessments, Cross-Chapter Synthesis)  
**Phase 3:** Full Next.js Web App with all features consolidated

### **1.4 Required Features (All Phases)**

1. **Content Delivery** - Serve course chapters verbatim
2. **Navigation** - Next/previous chapter sequencing
3. **Grounded Q&A** - Answer from content only
4. **Rule-Based Quizzes** - Multiple-choice with answer keys
5. **Progress Tracking** - Completion, streaks, achievements
6. **Freemium Gate** - Free: Chapters 1-3, Premium: All chapters

---

## **2. Development Principles**

### **2.1 Core Principles**

| Principle | Description | Enforcement |
|-----------|-------------|-------------|
| **Spec-First** | Write complete specs BEFORE any code | Manual approval required |
| **Test-Driven** | Write tests BEFORE implementation | 90% coverage required |
| **No Mocking** | Real database for all tests | SQLite in-memory for speed |
| **Document Everything** | Every decision, conversation, approval | Separate files per category |
| **No Blind Decisions** | Explicit permission for EVERYTHING | Chat-based approval workflow |
| **AI-Builder Model** | AI builds, User manages & orchestrates | AI points out issues immediately |

### **2.2 Golden Rules**

1. ✅ **Zero-Backend-LLM in Phase 1** - Backend NEVER calls LLM APIs
2. ✅ **Spec before Code** - No implementation without approved spec
3. ✅ **Test before Feature** - No feature without passing tests
4. ✅ **Document before Decision** - No decision without documentation
5. ✅ **Ask before Action** - No action without explicit permission

---

## **3. Technology Stack**

### **3.1 Backend (FastAPI - Python)**

| Component | Technology | Version | Why Chosen |
|-----------|-----------|---------|------------|
| **Framework** | FastAPI | Latest | High performance, auto OpenAPI docs, async support |
| **Python** | Python | 3.12 | Latest stable, best type hinting support |
| **Database ORM** | SQLModel | Latest | Combines SQLAlchemy + Pydantic, perfect for FastAPI |
| **Migrations** | Alembic | Latest | Standard SQLAlchemy migration tool |
| **Testing** | pytest | Latest | Simple syntax, powerful fixtures, best for FastAPI |
| **Test Coverage** | pytest-cov | Latest | Coverage reporting for pytest |
| **Code Quality** | ruff + black + mypy | Latest | Fast linting, formatting, type checking |
| **Pre-commit** | pre-commit | Latest | Auto-run checks before git commit |

**Why SQLModel?**
- Built by FastAPI creator
- Reduces boilerplate (one model for DB + validation)
- Full SQLAlchemy power
- Pydantic validation built-in

**Why pytest?**
- Simple, readable test syntax
- Powerful fixture system
- Great FastAPI integration
- Large ecosystem of plugins

### **3.2 ChatGPT App (Phase 1 & 2)**

| Component | Technology | Version | Why Chosen |
|-----------|-----------|---------|------------|
| **SDK** | OpenAI Apps SDK | Latest | Official SDK for ChatGPT apps |
| **Manifest** | YAML | N/A | ChatGPT app configuration |
| **Instructions** | Markdown | N/A | AI behavior specification |

### **3.3 Web App (Phase 3)**

| Component | Technology | Version | Why Chosen |
|-----------|-----------|---------|------------|
| **Framework** | Next.js | 14 (App Router) | Latest, React Server Components, best performance |
| **Language** | TypeScript | Latest | Type safety, better DX, catches errors early |
| **Styling** | Tailwind CSS | Latest | Utility-first, fast development, responsive |
| **Components** | shadcn/ui | Latest | Beautiful, accessible, customizable, no dependency hell |
| **Testing** | Playwright | Latest | E2E testing, cross-browser, reliable |
| **Linting** | ESLint + Prettier | Latest | Code quality + consistent formatting |

**Why Next.js 14 App Router?**
- Latest stable version
- Server Components for performance
- Built-in API routes
- Best Vercel integration

**Why shadcn/ui?**
- Not a component library (no npm install)
- Copy-paste components you own
- Built on Radix UI (accessible)
- Tailwind CSS native
- Fully customizable

### **3.4 Infrastructure**

| Component | Technology | Tier | Why Chosen |
|-----------|-----------|------|------------|
| **Database** | Supabase | Free | PostgreSQL, Auth, easy setup, generous free tier |
| **Backend Hosting** | Railway | Free | Easy deployment, auto-deploys from GitHub |
| **Web App Hosting** | Vercel | Free | Best for Next.js, auto-deploys, edge functions |
| **Content Storage** | Cloudflare R2 | Free | S3-compatible, no egress fees, cheap |
| **Version Control** | GitHub | Free | Standard, CI/CD integration |
| **Containerization** | Docker | Latest | Consistent environments |
| **Kubernetes** | Documented only | N/A | Mentioned in architecture doc, skipped for implementation |

**Docker & Kubernetes Decision:**
- ✅ **Docker:** Used for local development consistency
- ✅ **Kubernetes:** Documented in architecture (per hackathon doc) but NOT implemented
- **Why:** Overkill for this project scope, Railway/Vercel handle scaling

### **3.5 Authentication (Supabase Auth)**

| Method | Priority | Phase |
|--------|----------|-------|
| **Magic Links** | Primary | Phase 1 |
| **OAuth (Google, GitHub)** | Secondary | Phase 1 |
| **Email/Password** | Fallback | Phase 1 |

**Why Magic Links?**
- No password management
- Better security (no password reuse)
- Simpler UX
- Free with Supabase

### **3.6 Code Quality Tools**

| Tool | Purpose | When Runs |
|------|---------|-----------|
| **ruff** | Linting (fast, Rust-based) | Pre-commit, CI |
| **black** | Code formatting | Pre-commit, CI |
| **mypy** | Type checking | Pre-commit, CI |
| **pytest-cov** | Coverage reporting | Test run |
| **ESLint** | Frontend linting | Pre-commit, CI |
| **Prettier** | Frontend formatting | Pre-commit, CI |

---

## **4. Spec-Driven Development Process**

### **4.1 Spec Types & Locations**

```
specs/
├── functional/          # User-facing features (what it does)
│   ├── SPEC-F-001-content-delivery-v1.0.md
│   ├── SPEC-F-002-navigation-v1.0.md
│   └── ...
├── technical/           # Implementation details (how it works)
│   ├── SPEC-T-001-database-schema-v1.0.md
│   ├── SPEC-T-002-api-architecture-v1.0.md
│   └── ...
└── api/                 # API contracts (request/response)
    ├── SPEC-A-001-content-apis-v1.0.md
    ├── SPEC-A-002-quiz-apis-v1.0.md
    └── ...
```

### **4.2 Spec Naming Convention**

```
SPEC-{TYPE}-{NUMBER}-{feature}-v{MAJOR}.{MINOR}.md

Examples:
- SPEC-F-001-content-delivery-v1.0.md
- SPEC-T-001-database-schema-v1.0.md
- SPEC-A-001-content-apis-v1.0.md
```

### **4.3 Spec Template Structure**

Every spec MUST follow this template:

```markdown
# SPEC-{TYPE}-{NUMBER}-{feature}-v{VERSION}

## Status
- [ ] Draft
- [ ] Pending Approval
- [ ] Approved
- [ ] In Progress
- [ ] Completed
- [ ] Deprecated

## Metadata
- **Created:** YYYY-MM-DD
- **Author:** [Name]
- **Approved By:** [Name, Date]
- **Version:** X.Y.Z

## 1. Overview
What this spec covers (2-3 sentences)

## 2. Functional Requirements (Functional Specs Only)
- FR-1: ...
- FR-2: ...

## 3. Technical Requirements (Technical Specs Only)
- TR-1: ...
- TR-2: ...

## 4. API Contract (API Specs Only)
- Endpoint definitions
- Request/response schemas
- Error codes

## 5. User Stories
As a [user], I want [feature], so that [benefit]

## 6. Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## 7. Dependencies
What this spec depends on

## 8. Out of Scope
What this spec does NOT cover

## 9. Testing Requirements
- Test scenarios
- Coverage requirements

## 10. Open Questions
Unresolved issues

## 11. Revision History
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | YYYY-MM-DD | Initial draft | Name |
```

### **4.4 Spec Approval Process**

```
1. AI writes spec draft
2. AI asks for permission in chat
3. User reviews and approves/rejects
4. If approved: Update status to "Approved", add to approvals/
5. If rejected: Update status to "Draft", note feedback
6. Only approved specs can be implemented
```

### **4.5 Spec Versioning**

| Version Type | When to Increment | Example |
|--------------|-------------------|---------|
| **Major** | Breaking changes | v1.0 → v2.0 |
| **Minor** | New features (backward compatible) | v1.0 → v1.1 |
| **Patch** | Bug fixes, clarifications | v1.0 → v1.0.1 |

---

## **5. Test-Driven Development Process**

### **5.1 Testing Pyramid**

```
        /\
       /  \      E2E Tests (Playwright)
      /----\    
     /      \   Integration Tests (pytest + TestClient)
    /--------\  
   /          \ Unit Tests (pytest + functions)
  /------------\
```

### **5.2 Testing Framework Choice**

**Backend: pytest**

**Why pytest?**
- Simple, readable syntax
- Powerful fixture system for test setup
- Best FastAPI integration (TestClient)
- Large plugin ecosystem
- Built-in coverage support
- Industry standard for Python

**Frontend: Playwright**

**Why Playwright?**
- Cross-browser (Chrome, Firefox, Safari)
- Auto-wait for elements (no flaky tests)
- Trace viewer for debugging
- Mobile emulation
- Better than Cypress for Next.js

### **5.3 No Mocking Policy**

**STRICT RULE:** No mocking at all. All tests must use real code paths.

| Test Type | Database | External Services | Notes |
|-----------|----------|-------------------|-------|
| **Unit** | SQLite in-memory | Real calls | Fast, isolated |
| **Integration** | SQLite in-memory | Real calls | API endpoints |
| **E2E** | Supabase (test instance) | Real calls | Full user journey |

**SQLite In-Memory for Speed:**
- Real SQL database (not fake)
- Fast (no disk I/O)
- Per-test database (isolated)
- Migrations run normally

### **5.4 Test File Structure**

```
backend/
├── tests/
│   ├── conftest.py              # Shared fixtures
│   ├── test_content_api.py      # Content endpoint tests
│   ├── test_quiz_api.py         # Quiz endpoint tests
│   ├── test_progress_api.py     # Progress endpoint tests
│   └── test_auth.py             # Authentication tests

web-app/
├── tests/
│   ├── e2e/
│   │   ├── onboarding.spec.ts   # User onboarding flow
│   │   ├── learning.spec.ts     # Learning journey flow
│   │   └── quiz.spec.ts         # Quiz completion flow
│   └── integration/
│       └── api.spec.ts          # API integration tests
```

### **5.5 Test Coverage Requirements**

**Minimum 90% coverage required.**

```bash
# Backend coverage command
pytest --cov=backend --cov-report=html --cov-fail-under=90

# Frontend coverage command
npm run test:coverage -- --coverageThreshold='{"global":{"lines":90}}'
```

**Coverage Report Location:** `coverage/` folder (HTML report)

### **5.6 Test Naming Convention**

```python
def test_{feature}_{scenario}_{expected_result}():
    # Example:
    def test_content_delivery_free_user_can_access_chapter_1():
    def test_content_delivery_free_user_cannot_access_chapter_4():
    def test_quiz_submission_valid_answers_returns_score():
```

### **5.7 Test-First Workflow**

```
1. Write failing test (Red)
2. Write minimum code to pass (Green)
3. Refactor (Refactor)
4. Repeat

NEVER write implementation before test exists.
```

---

## **6. Decision Documentation Process**

### **6.1 Decision Record Locations**

All documentation is in the `docs/` folder:

```
docs/
├── decisions/              # Architecture Decision Records (ADRs)
│   ├── approved/           # Approved decisions
│   ├── rejected/           # Rejected decisions
│   ├── ADR-001-technology-stack.md
│   ├── ADR-002-database-choice.md
│   ├── ADR-003-auth-method.md
│   └── ...
│
├── logs/                   # Conversation Logs
│   ├── 2026-03-29-session.md
│   ├── 2026-03-30-session.md
│   └── ...
│
└── approvals/              # Approval Tracking
    ├── pending/            # Awaiting user approval
    ├── approved/           # Approved decisions
    │   ├── APPROVAL-001-spec-f-001.md
    │   └── ...
    └── rejected/           # Rejected decisions
        └── ...
```

### **6.2 ADR Template**

```markdown
# ADR-{NUMBER}-{title}

## Status
- [ ] Proposed
- [ ] Accepted
- [ ] Rejected
- [ ] Deprecated

## Metadata
- **Created:** YYYY-MM-DD
- **Decision Maker:** [User Name]
- **AI Advisor:** Qwen Code
- **Approval Reference:** approvals/approved/APPROVAL-{NUMBER}.md

## Context
What is the issue that requires a decision?

## Decision
What was decided?

## Options Considered

### Option 1: [Name]
**Pros:**
- ...

**Cons:**
- ...

### Option 2: [Name]
**Pros:**
- ...

**Cons:**
- ...

### Option 3: [Name] (CHOSEN)
**Pros:**
- ...

**Cons:**
- ...

## Consequences

### Positive
- ...

### Negative
- ...

### Risks
- ...

## Related Specs
- SPEC-{type}-{number}-{feature}

## Related Conversations
- logs/YYYY-MM-DD-session.md

## Revision History
| Date | Changes | Author |
|------|---------|--------|
| YYYY-MM-DD | Initial decision | Name |
```

### **6.3 Conversation Log Template**

```markdown
# Session Log: YYYY-MM-DD

## Metadata
- **Date:** YYYY-MM-DD
- **Time:** HH:MM - HH:MM
- **Participants:** [User], Qwen Code (AI)
- **Session Goal:** [What we aimed to accomplish]

## Conversation Summary

### Topic 1: [Title]
**Time:** HH:MM

**User:** [Question/request]

**AI:** [Response]

**Decision:** [What was decided]

**Action Items:**
- [ ] Task 1
- [ ] Task 2

### Topic 2: [Title]
...

## Decisions Made
| Decision ID | Topic | Outcome | Status |
|-------------|-------|---------|--------|
| DEC-001 | ... | ... | Approved |

## Files Created/Modified
| File | Action | Reason |
|------|--------|--------|
| path/to/file.md | Created | Spec for feature X |

## Next Session Plan
What will we work on next?
```

---

## **7. Approval Workflow**

### **7.1 What Requires Approval**

**EVERYTHING requires explicit approval:**

| Category | Examples | Approval Required? |
|----------|----------|-------------------|
| **Specs** | All functional, technical, API specs | ✅ YES |
| **Decisions** | Any architectural/technical decision | ✅ YES |
| **Code Changes** | Any implementation | ✅ YES |
| **File Creation** | New files/folders | ✅ YES |
| **Dependencies** | New npm/pip packages | ✅ YES |
| **Tests** | Test files and scenarios | ✅ YES |
| **Documentation** | Docs, READMEs, guides | ✅ YES |
| **Bug Fixes** | Even bug fixes | ✅ YES |
| **Refactoring** | Code improvements | ✅ YES |

### **7.2 Approval Request Format**

AI must ask explicitly in chat:

```
📋 **APPROVAL REQUEST**

**What:** [Brief description]
**Why:** [Reason/benefit]
**Files Affected:** [List]
**Risks:** [Any risks]
**Alternatives:** [If any]

Do you approve? (Yes/No/Modify)
```

### **7.3 Approval Tracking**

After user approval:

```markdown
# APPROVAL-{NUMBER}-{spec-or-decision-id}.md

## Metadata
- **Approval ID:** APPROVAL-001
- **Date:** YYYY-MM-DD
- **Approved By:** [User Name]
- **AI Requester:** Qwen Code

## What Was Approved
[Description]

## Approval Chat Log
[Copy of chat where approval was given]

## Related Files
- specs/functional/SPEC-F-001-xxx.md
- decisions/ADR-001-xxx.md

## Status
✅ APPROVED

## Timestamp
YYYY-MM-DD HH:MM:SS
```

### **7.4 Approval Workflow Diagram**

```
┌─────────────┐
│   AI        │
│   Identifies│
│   Need for  │
│   Decision  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   AI        │
│   Writes    │
│   Draft     │
│   (Spec/    │
│   Decision) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   AI        │
│   Requests  │
│   Approval  │
│   in Chat   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   User      │
│   Reviews   │
│   &         │
│   Decides   │
└──────┬──────┘
       │
       ├──────► NO ──────► Update Draft ──────► Repeat
       │
       ▼
      YES
       │
       ▼
┌─────────────┐
│   AI        │
│   Saves     │
│   Approval  │
│   to        │
│   approvals/│
│   approved/ │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   AI        │
│   Proceeds  │
│   with      │
│   Implementation│
└─────────────┘
```

---

## **8. File Structure**

### **8.1 Complete Project Structure**

```
hackathon-4/
│
├── QWEN.md                          # This file (operating manual)
├── README.md                        # Project overview
├── CONTRIBUTING.md                  # How to contribute
├── .gitignore                       # Git ignore rules
├── .pre-commit-config.yaml          # Pre-commit hooks
│
├── docs/                            # ALL DOCUMENTATION (specs, decisions, logs, approvals, skills)
│   ├── README.md                    # Docs folder guide
│   │
│   ├── specs/                       # Specification documents
│   │   ├── functional/              # User-facing feature specs
│   │   │   ├── SPEC-F-001-content-delivery-v1.0.md
│   │   │   ├── SPEC-F-002-navigation-v1.0.md
│   │   │   ├── SPEC-F-003-quiz-v1.0.md
│   │   │   ├── SPEC-F-004-progress-tracking-v1.0.md
│   │   │   ├── SPEC-F-005-grounded-qa-v1.0.md
│   │   │   └── SPEC-F-006-freemium-gate-v1.0.md
│   │   │
│   │   ├── technical/               # Implementation specs
│   │   │   ├── SPEC-T-001-database-schema-v1.0.md
│   │   │   ├── SPEC-T-002-auth-architecture-v1.0.md
│   │   │   ├── SPEC-T-003-content-storage-v1.0.md
│   │   │   └── SPEC-T-004-caching-strategy-v1.0.md
│   │   │
│   │   └── api/                     # API contract specs
│   │       ├── SPEC-A-001-content-apis-v1.0.md
│   │       ├── SPEC-A-002-quiz-apis-v1.0.md
│   │       ├── SPEC-A-003-progress-apis-v1.0.md
│   │       ├── SPEC-A-004-auth-apis-v1.0.md
│   │       └── SPEC-A-005-search-apis-v1.0.md
│   │
│   ├── decisions/                   # Architecture Decision Records (ADRs)
│   │   ├── approved/                # Approved decisions
│   │   ├── rejected/                # Rejected decisions
│   │   ├── ADR-001-technology-stack.md
│   │   └── TEMPLATE-ADR.md
│   │
│   ├── logs/                        # Conversation logs
│   │   ├── 2026-03-29-session.md
│   │   └── TEMPLATE-LOG.md
│   │
│   ├── approvals/                   # Approval tracking
│   │   ├── pending/                 # Awaiting approval
│   │   ├── approved/                # Approved items
│   │   ├── rejected/                # Rejected items
│   │   └── TEMPLATE-APPROVAL.md
│   │
│   └── skills/                      # Agent skills (AI tutor behaviors)
│       ├── concept-explainer.md
│       ├── quiz-master.md
│       ├── socratic-tutor.md
│       └── progress-motivator.md
│
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry
│   │   ├── config.py                # Configuration
│   │   ├── database.py              # Database connection
│   │   │
│   │   ├── api/                     # API routes
│   │   │   ├── __init__.py
│   │   │   ├── content.py
│   │   │   ├── quizzes.py
│   │   │   ├── progress.py
│   │   │   ├── auth.py
│   │   │   └── search.py
│   │   │
│   │   ├── models/                  # Database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── chapter.py
│   │   │   ├── quiz.py
│   │   │   └── progress.py
│   │   │
│   │   ├── schemas/                 # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── content.py
│   │   │   ├── quiz.py
│   │   │   └── progress.py
│   │   │
│   │   ├── services/                # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── content_service.py
│   │   │   ├── quiz_service.py
│   │   │   └── progress_service.py
│   │   │
│   │   └── skills/                  # Python skill implementations
│   │       ├── __init__.py
│   │       ├── content_search.py
│   │       └── quiz_grader.py
│   │
│   ├── tests/                       # Backend tests
│   │   ├── conftest.py
│   │   ├── test_content_api.py
│   │   ├── test_quiz_api.py
│   │   ├── test_progress_api.py
│   │   └── test_auth.py
│   │
│   ├── alembic/                     # Database migrations
│   │   ├── versions/
│   │   └── alembic.ini
│   │
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Backend container
│   └── docker-compose.yml           # Local dev environment
│
├── chatgpt-app/
│   ├── manifest.yaml                # ChatGPT app manifest
│   ├── instructions.md              # AI tutor instructions
│   └── README.md                    # ChatGPT app docs
│
├── web-app/                         # Next.js app (Phase 3)
│   ├── app/                         # App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── dashboard/
│   │   ├── chapters/
│   │   ├── quiz/
│   │   └── progress/
│   │
│   ├── components/                  # React components
│   │   ├── ui/                      # shadcn/ui components
│   │   ├── chapters/
│   │   ├── quiz/
│   │   └── progress/
│   │
│   ├── tests/                       # Frontend tests
│   │   ├── e2e/
│   │   └── integration/
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── Dockerfile
│
├── content/                         # Course content (local dev)
│   ├── generative-ai-fundamentals/
│   │   ├── chapter-01-intro.md
│   │   ├── chapter-02-llms.md
│   │   └── ...
│   └── metadata.json
│
├── docs_external/                   # External documentation (generated)
│   ├── ARCHITECTURE.md              # System architecture
│   ├── DEPLOYMENT.md                # Deployment guide
│   ├── API.md                       # API documentation
│   └── CHANGELOG.md                 # Version history
│
├── coverage/                        # Test coverage reports
│   ├── backend/
│   └── frontend/
│
└── .github/
    └── workflows/
        └── ci.yml                   # GitHub Actions CI/CD
```

### **8.2 File Naming Conventions**

| File Type | Convention | Example |
|-----------|------------|---------|
| **Specs** | `SPEC-{TYPE}-{NUM}-{feature}-v{version}.md` | `SPEC-F-001-content-delivery-v1.0.md` |
| **ADRs** | `ADR-{NUM}-{title}.md` | `ADR-001-technology-stack.md` |
| **Logs** | `YYYY-MM-DD-session.md` | `2026-03-29-session.md` |
| **Approvals** | `APPROVAL-{NUM}-{ref}.md` | `APPROVAL-001-spec-f-001.md` |
| **Tests** | `test_{feature}.py` | `test_content_api.py` |
| **Models** | `{entity}.py` | `user.py`, `chapter.py` |
| **APIs** | `{feature}.py` | `content.py`, `quiz.py` |

---

## **9. Communication Protocol**

### **9.1 AI Behavior**

| Situation | AI Action |
|-----------|-----------|
| **Building features** | Ask permission before each step |
| **Seeing potential issues** | Point out immediately |
| **User makes spec violation** | Point out immediately |
| **Unclear requirement** | Ask clarifying questions |
| **Multiple options exist** | Present all options with pros/cons |
| **Decision needed** | Create decision draft, request approval |
| **Spec needed** | Write spec draft, request approval |
| **Test failing** | Report immediately, don't proceed |

### **9.2 User Role (Manager/Orchestrator)**

- Review and approve/reject specs
- Make final decisions on options
- Provide course content direction
- Validate feature implementations
- Approve deployment steps

### **9.3 AI Role (Builder)**

- Write all specs (drafts)
- Write all code
- Write all tests
- Write all documentation
- Point out issues immediately
- Never proceed without approval
- Maintain decision logs

### **9.4 Chat Communication Format**

**For Approval Requests:**
```
📋 **APPROVAL REQUEST**

**What:** [Description]
**Why:** [Reason]
**Files:** [List]
**Risks:** [Any]

Approve? (Yes/No/Modify)
```

**For Decisions:**
```
🤔 **DECISION NEEDED**

**Topic:** [What needs deciding]
**Options:**
1. [Option A] - Pros/Cons
2. [Option B] - Pros/Cons

**Recommendation:** [AI suggestion]

Your decision?
```

**For Issues:**
```
⚠️ **ISSUE DETECTED**

**What:** [Problem]
**Impact:** [Effect]
**Location:** [File/feature]
**Suggestion:** [Fix]

Proceed with fix? (Yes/No)
```

---

## **10. Quality Standards**

### **10.1 Code Quality**

**Backend (Python):**
- ✅ Type hints on all functions
- ✅ Docstrings for public functions
- ✅ Follow PEP 8 style
- ✅ Max function length: 50 lines
- ✅ Max file length: 500 lines

**Frontend (TypeScript):**
- ✅ TypeScript strict mode
- ✅ No `any` type (use proper types)
- ✅ Components < 200 lines
- ✅ Props interfaces documented

### **10.2 Pre-commit Hooks**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

### **10.3 CI/CD Pipeline (GitHub Actions)**

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Run tests with coverage
        run: pytest --cov=backend --cov-fail-under=90
      - name: Lint
        run: ruff check backend && black --check backend

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm run test
      - name: Lint
        run: npm run lint
```

---

## **11. Security Guidelines**

### **11.1 Authentication (Supabase Auth)**

**Implementation:**
- Magic links (primary)
- OAuth (Google, GitHub)
- Email/password (fallback)

**Security Features:**
- JWT tokens (short-lived)
- Refresh tokens (rotating)
- Rate limiting on auth endpoints
- HTTPS only
- Secure cookie storage

### **11.2 API Security**

| Measure | Implementation |
|---------|---------------|
| **Authentication** | Supabase Auth JWT |
| **Authorization** | Role-based access control |
| **Rate Limiting** | SlowAPI (100 req/min per user) |
| **CORS** | Whitelist domains only |
| **Input Validation** | Pydantic schemas |
| **SQL Injection** | SQLAlchemy ORM (parameterized) |
| **XSS** | React escapes by default |

### **11.3 Secrets Management**

```bash
# .env (gitignored)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
DATABASE_URL=postgresql://...
SECRET_KEY=your_secret_key
CLOUDFLARE_R2_ENDPOINT=...
CLOUDFLARE_R2_ACCESS_KEY=...
CLOUDFLARE_R2_SECRET_KEY=...
```

**Rules:**
- ✅ Never commit `.env` files
- ✅ Use GitHub Secrets for CI/CD
- ✅ Rotate secrets every 90 days
- ✅ Different secrets for dev/staging/prod

### **11.4 Data Privacy**

| Data Type | Storage | Retention |
|-----------|---------|-----------|
| **User Email** | Supabase Auth | Until account deletion |
| **Progress Data** | Supabase DB | Until account deletion |
| **Quiz Scores** | Supabase DB | Until account deletion |
| **Session Logs** | Not stored | N/A |
| **Analytics** | None (Phase 1) | N/A |

**GDPR Considerations:**
- Users can request data export
- Users can request account deletion
- Minimal data collection
- No third-party tracking (Phase 1)

---

## **12. Deployment Strategy**

### **12.1 Environments**

| Environment | Purpose | Backend | Frontend | Database |
|-------------|---------|---------|----------|----------|
| **Local** | Development | Docker | localhost | SQLite |
| **Production** | Live users | Railway | Vercel | Supabase |

**Note:** No staging environment (use free tiers only)

### **12.2 Backend Deployment (Railway)**

```yaml
# railway.toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "backend/Dockerfile"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 100
```

**Steps:**
1. Connect GitHub repo to Railway
2. Set environment variables
3. Auto-deploy on push to main

### **12.3 Frontend Deployment (Vercel)**

```json
// vercel.json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install"
}
```

**Steps:**
1. Connect GitHub repo to Vercel
2. Set environment variables
3. Auto-deploy on push to main

### **12.4 Database Setup (Supabase)**

```sql
-- Run migrations via Alembic
alembic upgrade head

-- Enable Auth
-- Enable Row Level Security (RLS)
-- Create policies
```

### **12.5 Content Storage (Cloudflare R2)**

```python
# Upload course content to R2 bucket
# Access via S3-compatible API
# Serve via public URLs
```

### **12.6 Docker Configuration**

**Backend Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Docker Compose (Local Dev):**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///:memory:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
    volumes:
      - ./backend:/app

  frontend:
    build: ./web-app
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./web-app:/app
```

---

## **13. Monitoring & Maintenance**

### **13.1 What is Monitoring?**

**Monitoring** = Watching your application to ensure it's working correctly.

**Why we need it:**
- Catch errors before users report them
- Know when something breaks
- Track performance issues
- Understand usage patterns

### **13.2 What We'll Monitor**

| Category | Metrics | Tool |
|----------|---------|------|
| **Errors** | API errors, crashes | Railway logs |
| **Performance** | Response times | Railway metrics |
| **Uptime** | Is service running? | Railway health checks |
| **Database** | Connection errors | Supabase dashboard |
| **Usage** | API calls per day | Railway logs |

### **13.3 What is Analytics?**

**Analytics** = Tracking how users interact with your app.

**Why we need it:**
- See which chapters users complete
- Find where users drop off
- Identify difficult quiz questions
- Measure engagement

### **13.4 Analytics Decision**

**Phase 1:** No external analytics (privacy-first, free tiers)

**Track Manually:**
- Chapter completions (in database)
- Quiz scores (in database)
- User streaks (in database)

**Phase 2:** Consider privacy-friendly analytics (Plausible)

**Why no Google Analytics?**
- Privacy concerns
- Cookie consent complexity
- Not needed for MVP
- Can add later

### **13.5 Health Check Endpoints**

```python
# GET /health
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-03-29T10:00:00Z"
}
```

```python
# GET /ready
{
  "status": "ready",
  "supabase": "connected",
  "r2": "connected"
}
```

### **13.6 Logging Strategy**

```python
# Use Python logging
import logging

logger = logging.getLogger(__name__)

logger.info("User completed chapter")
logger.warning("User failed quiz 3 times")
logger.error("Database connection failed")
```

**Log Levels:**
- `DEBUG`: Detailed info for debugging
- `INFO`: Normal operations
- `WARNING`: Something unexpected but handled
- `ERROR`: Something broke
- `CRITICAL`: System down

---

## **14. Appendices**

### **Appendix A: Accessibility Requirements**

**What is Accessibility?**
Making your app usable by people with disabilities:
- Visual impairments (blindness, color blindness)
- Motor impairments (can't use mouse)
- Cognitive impairments (learning disabilities)
- Hearing impairments

**Why do we need it?**
- **Ethical:** Everyone should access education
- **Legal:** Required by law in many countries
- **Business:** Larger audience
- **SEO:** Accessible sites rank better

**What We'll Implement (WCAG 2.1 AA):**

| Requirement | Implementation |
|-------------|---------------|
| **Keyboard Navigation** | All features work without mouse |
| **Screen Reader Support** | Proper ARIA labels, semantic HTML |
| **Color Contrast** | Text readable (4.5:1 ratio) |
| **Focus Indicators** | Visible focus rings on buttons/links |
| **Alt Text** | Descriptions for images/diagrams |
| **Form Labels** | All inputs have labels |
| **Error Messages** | Clear, descriptive error text |

**shadcn/ui Benefit:** All components are accessible by default (built on Radix UI)

### **Appendix B: Glossary**

| Term | Definition |
|------|------------|
| **FTE** | Full-Time Equivalent (168 hours/week) |
| **Zero-Backend-LLM** | Backend makes no LLM calls |
| **Hybrid Intelligence** | Backend + LLM API calls for premium features |
| **Spec-Driven** | Write specifications before code |
| **TDD** | Test-Driven Development (tests before code) |
| **ADR** | Architecture Decision Record |
| **R2** | Cloudflare object storage (S3-compatible) |
| **MCP** | Model Context Protocol (AI tool integration) |
| **A2A** | Agent-to-Agent protocol |

### **Appendix C: Quick Reference Commands**

**Backend:**
```bash
# Run tests
pytest --cov=backend --cov-report=html

# Run with coverage requirement
pytest --cov=backend --cov-fail-under=90

# Lint code
ruff check backend
black --check backend
mypy backend

# Run database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head

# Start local server
uvicorn app.main:app --reload
```

**Frontend:**
```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Run tests
npm run test

# Run E2E tests
npm run test:e2e

# Build for production
npm run build

# Lint code
npm run lint
```

**Pre-commit:**
```bash
# Install pre-commit hooks
pre-commit install

# Run all hooks manually
pre-commit run --all-files
```

### **Appendix D: Hackathon Deliverables Checklist**

| Deliverable | Location | Status |
|-------------|----------|--------|
| Source Code | GitHub repo | [ ] |
| Architecture Diagram | docs/ARCHITECTURE.md | [ ] |
| Spec Documents | specs/ | [ ] |
| Cost Analysis | docs/COST-ANALYSIS.md | [ ] |
| Demo Video (5 min) | video/ | [ ] |
| API Documentation | docs/API.md (OpenAPI) | [ ] |
| ChatGPT App Manifest | chatgpt-app/manifest.yaml | [ ] |
| SKILL.md files | skills/ | [ ] |
| QWEN.md | QWEN.md | ✅ |

### **Appendix E: Revision History**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2026-03-29 | Initial creation | Qwen Code |

---

## **Document Approval**

| Role | Name | Date | Signature |
|------|------|------|-----------|
| **Project Manager** | [User] | | |
| **AI Builder** | Qwen Code | 2026-03-29 | ✅ |

---

**END OF QWEN.md**

*This document is the single source of truth for how this project operates. All team members (current and future) must read and follow this guide.*

*Last Updated: March 29, 2026*
