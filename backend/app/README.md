# Backend Application

This folder contains the FastAPI backend application.

## Structure

```
app/
├── main.py                  # FastAPI app entry point
├── config.py                # Configuration settings
├── database.py              # Database connection
├── api/                     # API routes
│   ├── __init__.py
│   ├── content.py           # Content endpoints
│   ├── quizzes.py           # Quiz endpoints
│   ├── progress.py          # Progress endpoints
│   ├── auth.py              # Auth endpoints
│   └── search.py            # Search endpoints
├── models/                  # Database models
│   ├── __init__.py
│   ├── user.py
│   ├── chapter.py
│   ├── quiz.py
│   └── progress.py
├── schemas/                 # Pydantic schemas
│   ├── __init__.py
│   ├── content.py
│   ├── quiz.py
│   └── progress.py
├── services/                # Business logic
│   ├── __init__.py
│   ├── content_service.py
│   ├── quiz_service.py
│   └── progress_service.py
└── skills/                  # Python skill implementations
    ├── __init__.py
    ├── content_search.py
    └── quiz_grader.py
```

## Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Testing

```bash
pytest --cov=app --cov-report=html --cov-fail-under=90
```

---

*Last Updated: March 29, 2026*
