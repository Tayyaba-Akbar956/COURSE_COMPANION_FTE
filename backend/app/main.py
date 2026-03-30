"""
Course Companion FTE - FastAPI Backend

A 24/7 AI-powered digital tutor for Generative AI Fundamentals.
Phase 1: Zero-Backend-LLM Architecture
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import engine, create_db_and_tables
from app.api import chapters, quizzes, progress, auth, search
from app.middleware.error_handler import global_error_handler
from app.middleware.rate_limit import limiter, RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Course Companion FTE Backend...")
    await create_db_and_tables()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Course Companion FTE Backend...")
    engine.dispose()


# Create FastAPI app
app = FastAPI(
    title="Course Companion FTE API",
    description="API for Generative AI Fundamentals Course - Phase 1 (Zero-Backend-LLM)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add rate limiter
app.state.limiter = limiter

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add HTTPS redirect in production
if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)


# Register exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    return await global_error_handler(request, exc)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit exceeded"""
    return await global_error_handler(request, exc)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    return await global_error_handler(request, exc)


# Register API routes
app.include_router(chapters.router, prefix="/api/v1", tags=["Chapters"])
app.include_router(quizzes.router, prefix="/api/v1", tags=["Quizzes"])
app.include_router(progress.router, prefix="/api/v1", tags=["Progress"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Course Companion FTE API",
        "version": "1.0.0",
        "description": "Zero-Backend-LLM API for Generative AI Fundamentals course",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development"
    )
