"""
Error handling middleware

Global error handler for all API endpoints.
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import uuid
import logging

from app.schemas.chapter import MetaInfo, ErrorDetail

logger = logging.getLogger(__name__)


def get_error_code(status_code: int) -> str:
    """Map status code to error code"""
    mapping = {
        400: "INVALID_REQUEST",
        401: "UNAUTHORIZED",
        403: "ACCESS_DENIED",
        404: "NOT_FOUND",
        422: "VALIDATION_ERROR",
        429: "RATE_LIMIT_EXCEEDED",
        500: "INTERNAL_ERROR",
    }
    return mapping.get(status_code, "UNKNOWN_ERROR")


async def global_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global error handling function"""
    request_id = str(uuid.uuid4())
    
    if isinstance(exc, HTTPException):
        # Handle known HTTP exceptions
        logger.warning(f"HTTP {exc.status_code}: {exc.detail} (Request: {request_id})")
        
        error_code = get_error_code(exc.status_code)
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": error_code,
                    "message": exc.detail,
                },
                "meta": {
                    "request_id": request_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "execution_time_ms": 0
                }
            }
        )
    
    # Handle unexpected exceptions
    logger.error(f"Unexpected error: {str(exc)} (Request: {request_id})", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
            },
            "meta": {
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "execution_time_ms": 0
            }
        }
    )
