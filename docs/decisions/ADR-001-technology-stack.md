# ADR-001-technology-stack

## Status
✅ Accepted

## Metadata
- **Created:** 2026-03-29
- **Decision Maker:** User (Project Manager)
- **AI Advisor:** Qwen Code
- **Approval Reference:** approvals/approved/APPROVAL-001-technology-stack.md

## Context

We need to select the complete technology stack for building the Course Companion FTE - Generative AI Fundamentals. This decision will impact:
- Development speed and experience
- Performance and scalability
- Cost structure (must use free tiers)
- Maintainability
- Hackathon success

## Decision

Selected complete technology stack as documented in QWEN.md Section 3.

## Options Considered

### Backend Framework

#### Option 1: FastAPI (Python) ✅ CHOSEN
**Pros:**
- High performance (async support)
- Automatic OpenAPI documentation
- Type-safe with Pydantic
- Easy to learn and use
- Perfect for AI/ML projects
- Strong community support

**Cons:**
- Newer than Django (less battle-tested)
- Smaller ecosystem than Django

#### Option 2: Django + Django REST Framework
**Pros:**
- Very mature and stable
- Built-in admin panel
- Large ecosystem
- "Batteries included"

**Cons:**
- Heavier weight
- Slower than FastAPI
- More boilerplate code
- Overkill for our API-only needs

#### Option 3: Flask
**Pros:**
- Simple and lightweight
- Large ecosystem
- Very flexible

**Cons:**
- No built-in async support
- More manual configuration
- Less type safety
- Need more extensions

### Database ORM

#### Option 1: SQLModel ✅ CHOSEN
**Pros:**
- Built by FastAPI creator
- Combines SQLAlchemy + Pydantic
- One model for DB and validation
- Full SQLAlchemy power
- Less boilerplate

**Cons:**
- Newer (less documentation)
- Smaller community

#### Option 2: SQLAlchemy (standalone)
**Pros:**
- Very mature
- Huge community
- Maximum flexibility

**Cons:**
- More boilerplate
- Separate Pydantic models needed
- Steeper learning curve

#### Option 3: Tortoise ORM
**Pros:**
- Async native
- Django-like syntax

**Cons:**
- Smaller community
- Less documentation
- Not as mature

### Testing Framework

#### Option 1: pytest ✅ CHOSEN
**Pros:**
- Simple, readable syntax
- Powerful fixture system
- Best FastAPI integration
- Large plugin ecosystem
- Built-in coverage support
- Industry standard

**Cons:**
- Different from unittest (learning curve)

#### Option 2: unittest (built-in)
**Pros:**
- Built into Python
- No dependencies
- Familiar to Java developers

**Cons:**
- Verbose syntax
- Less powerful than pytest
- No fixtures
- Harder to read

#### Option 3: nose2
**Pros:**
- Plugin-based
- Auto-discovery

**Cons:**
- Less popular than pytest
- Smaller community

### Frontend Framework

#### Option 1: Next.js 14 (App Router) ✅ CHOSEN
**Pros:**
- Latest stable version
- Server Components for performance
- Built-in API routes
- Best Vercel integration
- Great for SEO
- Active development

**Cons:**
- New paradigm (learning curve)
- Breaking changes between versions

#### Option 2: Next.js 13 (Pages Router)
**Pros:**
- More stable
- Larger community
- More tutorials

**Cons:**
- Older paradigm
- Less performant
- Will be deprecated

#### Option 3: React (standalone)
**Pros:**
- Maximum flexibility
- No framework constraints
- Huge ecosystem

**Cons:**
- Need to set up routing
- No SSR by default
- More configuration
- Worse SEO

### Styling Solution

#### Option 1: Tailwind CSS ✅ CHOSEN
**Pros:**
- Utility-first (fast development)
- Highly customizable
- Small bundle size
- Great with TypeScript
- Responsive by default

**Cons:**
- Different paradigm (CSS-in-JS fans may dislike)
- Verbose class names

#### Option 2: CSS Modules
**Pros:**
- Scoped styles
- Familiar CSS syntax
- No runtime

**Cons:**
- More boilerplate
- Less reusable
- No design system

#### Option 3: Styled Components
**Pros:**
- CSS-in-JS
- Dynamic styling
- Theming support

**Cons:**
- Runtime overhead
- Larger bundle size
- Debugging can be hard

### Component Library

#### Option 1: shadcn/ui ✅ CHOSEN
**Pros:**
- Not a dependency (copy-paste)
- You own the code
- Built on Radix UI (accessible)
- Tailwind native
- Fully customizable
- Beautiful by default

**Cons:**
- Need to copy components manually
- More initial setup

#### Option 2: Material UI
**Pros:**
- Comprehensive
- Well-documented
- Large community

**Cons:**
- Heavy bundle size
- Hard to customize
- Distinctive look (hard to make unique)

#### Option 3: Chakra UI
**Pros:**
- Easy to use
- Good defaults
- Theming support

**Cons:**
- Runtime overhead
- Larger bundle
- Less customizable

### Authentication

#### Option 1: Supabase Auth (Magic Links + OAuth) ✅ CHOSEN
**Pros:**
- Free tier generous
- Magic links (no passwords)
- OAuth built-in
- JWT tokens
- Easy integration
- Secure by default

**Cons:**
- Vendor lock-in
- Less control than self-hosted

#### Option 2: NextAuth.js
**Pros:**
- Open source
- Many providers
- Self-hosted

**Cons:**
- More setup
- Need to manage secrets
- More maintenance

#### Option 3: Clerk
**Pros:**
- Very easy
- Great UX
- Many features

**Cons:**
- More expensive
- Less control
- Vendor lock-in

### Hosting

#### Backend: Railway ✅ CHOSEN
**Pros:**
- Free tier available
- Auto-deploys from GitHub
- Easy setup
- Good performance
- Simple pricing

**Cons:**
- Less control than VPS
- Limited free tier hours

#### Frontend: Vercel ✅ CHOSEN
**Pros:**
- Best for Next.js
- Free tier generous
- Edge functions
- Auto-deploys
- Great analytics

**Cons:**
- Vendor lock-in
- Serverless limits

### Database Hosting

#### Option 1: Supabase ✅ CHOSEN
**Pros:**
- Free tier (500MB)
- PostgreSQL
- Auth included
- Real-time features
- Easy to use

**Cons:**
- Vendor lock-in
- Limited free tier

#### Option 2: Neon
**Pros:**
- Serverless PostgreSQL
- Free tier
- Branching

**Cons:**
- Newer company
- Less features than Supabase

#### Option 3: Railway PostgreSQL
**Pros:**
- Integrated with backend
- Easy setup

**Cons:**
- Less features than Supabase
- No auth included

## Consequences

### Positive
- Modern, type-safe stack
- Excellent developer experience
- Fast performance
- Free tier viable
- Scalable architecture
- Great documentation auto-generated
- Accessible components by default

### Negative
- Multiple new technologies to learn
- Dependency on multiple vendors (Supabase, Railway, Vercel)
- Next.js 14 App Router has breaking changes
- SQLModel is newer (less documentation)

### Risks
- Free tier limits may be hit
- Vendor pricing changes
- Technology churn (Next.js changes frequently)
- Team learning curve

## Related Specs

- SPEC-T-001-database-schema-v1.0.md (pending)
- SPEC-T-002-auth-architecture-v1.0.md (pending)
- SPEC-A-001-content-apis-v1.0.md (pending)

## Related Conversations

- logs/2026-03-29-session.md

## Revision History

| Date | Changes | Author |
|------|---------|--------|
| 2026-03-29 | Initial decision | Qwen Code |
