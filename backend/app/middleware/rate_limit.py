"""
Rate limiting middleware

Prevents API abuse using slowapi.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)


async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit exceeded"""
    return JSONResponse(
        status_code=429,
        content={
            "success": False,
            "error": {
                "code": "RATE_LIMIT_EXCEEDED",
                "message": "Too many requests. Please try again later.",
                "retry_after": 30  # seconds
            },
            "meta": {
                "request_id": str(id(request)),
                "timestamp": datetime.utcnow().isoformat(),
                "execution_time_ms": 0
            }
        }
    )
