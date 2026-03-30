# Backend - FastAPI Course Companion API

FastAPI backend for the Course Companion FTE - Generative AI Fundamentals.

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- pip

### Installation

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env
# Edit .env with your configuration
```

### Run Locally

```bash
# Start development server
uvicorn app.main:app --reload

# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Run Tests

```bash
# Run all tests with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_chapters_api.py -v

# Run with coverage requirement (90%)
pytest --cov=app --cov-fail-under=90
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration management
│   ├── database.py             # Database connection
│   ├── security.py             # JWT utilities
│   │
│   ├── api/                    # API routes
│   │   ├── chapters.py         # Chapter endpoints
│   │   ├── quizzes.py          # Quiz endpoints
│   │   ├── progress.py         # Progress endpoints
│   │   ├── auth.py             # Auth endpoints
│   │   └── search.py           # Search endpoints
│   │
│   ├── models/                 # SQLModel database models
│   │   ├── user.py             # User, Subscription models
│   │   ├── chapter.py          # Module, Chapter models
│   │   ├── progress.py         # ChapterProgress, QuizQuestion, QuizAttempt
│   │   └── achievement.py      # Achievement, UserAchievement, DailyStreak
│   │
│   ├── schemas/                # Pydantic schemas
│   │   └── chapter.py          # All request/response schemas
│   │
│   └── middleware/             # Custom middleware
│       ├── error_handler.py    # Global error handling
│       └── rate_limit.py       # Rate limiting
│
├── tests/                      # Pytest tests
│   ├── conftest.py             # Shared fixtures
│   ├── test_smoke.py           # Smoke tests
│   ├── test_chapters_api.py    # Chapter API tests
│   └── test_quizzes_api.py     # Quiz API tests
│
├── alembic/                    # Database migrations
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Database
DATABASE_URL=sqlite+aiosqlite:///./course_companion.db
# For production: postgresql+asyncpg://user:password@host:port/db

# JWT Settings
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Supabase (Phase 2+)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 📡 API Endpoints

### Chapters

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/chapters` | List all chapters | Optional |
| GET | `/api/v1/chapters/{id}` | Get chapter details | Optional (Premium for paid chapters) |
| POST | `/api/v1/chapters/{id}/complete` | Mark chapter complete | Required |
| GET | `/api/v1/chapters/{id}/quiz` | Get quiz for chapter | Required |
| GET | `/api/v1/chapters/{id}/quiz/history` | Get quiz history | Required |

### Quizzes

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/chapters/quizzes/{id}/submit` | Submit quiz answers | Required |

### Progress

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/progress` | Get user progress | Required |
| GET | `/api/v1/progress/streak` | Get daily streak | Required |
| GET | `/api/v1/progress/achievements` | Get achievements | Required |

### Auth

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/signup` | Sign up new user | No |
| POST | `/api/v1/auth/login` | Login user | No |
| POST | `/api/v1/auth/refresh` | Refresh token | No |

### Search

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/search` | Search content | Optional |

## 🧪 Testing

### Test Fixtures

The test suite provides several fixtures in `conftest.py`:

- `client` - Async HTTP test client
- `test_db` - In-memory SQLite database session
- `sample_user` - Test user
- `sample_premium_user` - Premium test user
- `sample_module` - Test module
- `sample_chapter` - Test chapter
- `sample_quiz_question` - Test quiz question
- `valid_token` - Valid JWT token
- `premium_token` - Premium user JWT token
- `auth_headers` - Authorization headers
- `premium_auth_headers` - Premium user authorization headers

### Example Test

```python
@pytest.mark.anyio
async def test_get_chapter(client: AsyncClient, sample_chapter, auth_headers):
    """Test getting a chapter"""
    response = await client.get(
        f"/api/v1/chapters/{sample_chapter.id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
```

## 🗄️ Database

### Models

- **User** - User account
- **Subscription** - User subscription tier
- **Module** - Course module (6 total)
- **Chapter** - Course chapter (24 total)
- **ChapterProgress** - User chapter completion
- **QuizQuestion** - Quiz question bank
- **QuizAttempt** - User quiz attempts
- **Achievement** - Achievement definitions
- **UserAchievement** - Unlocked achievements
- **DailyStreak** - Daily activity tracking

### Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 🚨 Error Handling

All errors return a consistent format:

```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Chapter not found"
  },
  "meta": {
    "request_id": "uuid",
    "timestamp": "2026-03-30T10:00:00Z",
    "execution_time_ms": 45
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_REQUEST` | 400 | Bad request |
| `UNAUTHORIZED` | 401 | Authentication required |
| `ACCESS_DENIED` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 422 | Invalid input |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |

## 🔐 Authentication

### JWT Tokens

The backend uses JWT tokens for authentication:

```python
# Create token
from app.security import create_access_token

token = await create_access_token(
    data={"user_id": "user-123", "email": "user@example.com"}
)

# Verify token
from app.security import verify_token

payload = await verify_token(token)
```

### Usage

Include token in Authorization header:

```
Authorization: Bearer <token>
```

## 📊 Test Results

```
======================== 24 passed ========================
- Smoke Tests: 2/2 ✅
- Chapter API Tests: 13/13 ✅
- Quiz API Tests: 9/9 ✅

Coverage: 100% passing
```

## 🛠️ Development

### Code Quality

```bash
# Lint
ruff check app

# Format
black app

# Type check
mypy app
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

## 📦 Dependencies

See `requirements.txt` for full list:

- **fastapi** - Web framework
- **sqlmodel** - Database ORM
- **pydantic** - Data validation
- **pytest** - Testing framework
- **httpx** - Async HTTP client
- **python-jose** - JWT handling
- **aiosqlite** - Async SQLite
- **uvicorn** - ASGI server

## 🚀 Deployment

### Railway

1. Connect GitHub repository
2. Set environment variables
3. Deploy automatically on push

### Docker

```bash
# Build
docker build -t course-companion-backend .

# Run
docker run -p 8000:8000 --env-file .env course-companion-backend
```

## 📝 API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🆘 Troubleshooting

### Common Issues

**Database locked:**
```bash
# Delete SQLite database
rm course_companion.db
# Restart server
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Test failures:**
```bash
# Clear pytest cache
pytest --cache-clear
```

## 📚 Related

- [Project Overview](../README.md)
- [Architecture](../docs_external/ARCHITECTURE.md)
- [API Documentation](../docs_external/API.md)
