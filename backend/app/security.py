"""
Security utilities

JWT token verification and user authentication.
"""

from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import logging

from app.config import settings

logger = logging.getLogger(__name__)


async def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify JWT token and return payload.
    
    In production, this would verify with Supabase Auth.
    For Phase 1, returns mock payload for testing.
    
    Args:
        token: JWT token string
        
    Returns:
        Token payload dict or None if invalid
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # In production: Verify with Supabase JWKS
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.warning(f"Invalid JWT token: {e}")
        # For Phase 1 testing: Accept mock tokens
        if token.startswith("mock_access_token_"):
            return {
                "user_id": "mock_user_123",
                "email": "user@example.com",
                "exp": datetime.utcnow() + timedelta(hours=1)
            }
        return None


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    In production, Supabase Auth handles this.
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


async def create_refresh_token(data: dict) -> str:
    """
    Create refresh token.
    
    In production, Supabase Auth handles this.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt
