"""
Auth API Router

Endpoints for authentication using Supabase Auth.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import uuid

from app.database import get_db
from app.models.user import User, Subscription
from app.schemas.chapter import (
    SignupRequest,
    LoginRequest,
    AuthResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    UserInfoResponse,
    UserInfo,
    ERROR_CODES
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """
    Create new user account (sends magic link).
    
    In production, this would trigger Supabase Auth to send magic link.
    """
    # For Phase 1, we'll simulate magic link
    # In production: Use Supabase Auth SDK
    
    return AuthResponse(
        success=True,
        message=f"Magic link sent to {request.email}",
        email=request.email
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """
    Login with magic link.
    
    In production, this would verify magic link token from Supabase Auth.
    """
    # For Phase 1, we'll simulate login
    # In production: Use Supabase Auth SDK
    
    return AuthResponse(
        success=True,
        message=f"Magic link sent to {request.email}",
        email=request.email
    )


@router.post("/oauth/{provider}")
async def oauth_login(provider: str, request: Request):
    """
    Initiate OAuth login (Google, GitHub).
    
    Returns OAuth URL for redirect.
    """
    if provider not in ["google", "github"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported OAuth provider"
        )
    
    # In production: Use Supabase Auth OAuth
    oauth_url = f"https://your-project.supabase.co/auth/v1/authorize?provider={provider}"
    
    return {
        "success": True,
        "oauth_url": oauth_url
    }


@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_token(request: TokenRefreshRequest):
    """
    Refresh access token using refresh token.
    
    In production, this would validate refresh token with Supabase.
    """
    # For Phase 1, return mock token
    # In production: Use Supabase Auth SDK
    
    return TokenRefreshResponse(
        access_token="mock_access_token_" + uuid.uuid4().hex,
        expires_in=3600,
        token_type="Bearer"
    )


@router.post("/logout")
async def logout():
    """
    Logout user (revoke refresh token).
    """
    # In production: Revoke token with Supabase
    
    return {
        "success": True,
        "message": "Logged out successfully"
    }


@router.get("/me", response_model=UserInfoResponse)
async def get_current_user_info(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user information.
    
    Requires valid JWT token in Authorization header.
    """
    # Extract token from header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail=ERROR_CODES["UNAUTHORIZED"]["message"]
        )
    
    token = auth_header.replace("Bearer ", "")
    
    # In production: Verify token with Supabase
    # For Phase 1: Return mock user
    user_id = "mock_user_" + uuid.uuid4().hex[:8]
    
    return UserInfoResponse(
        success=True,
        data=UserInfo(
            user_id=user_id,
            email="user@example.com",
            full_name="Demo User",
            subscription_tier="free",
            created_at=datetime.utcnow()
        )
    )


@router.post("/password/reset")
async def reset_password(request: dict):
    """
    Request password reset (for email/password users).
    """
    email = request.get("email")
    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email required"
        )
    
    # In production: Send reset email via Supabase Auth
    
    return {
        "success": True,
        "message": f"Password reset link sent to {email}"
    }
