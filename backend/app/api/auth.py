"""
Auth API Router

Endpoints for authentication using Supabase Auth.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from uuid import uuid4
import uuid

from app.database import get_db
from app.models.user import User, Subscription, SubscriptionTier
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
from app.security import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest, db: AsyncSession = Depends(get_db)):
    """
    Create new user account.

    For Phase 1 testing: Creates user and returns JWT token.
    In production: Would use Supabase Auth magic links.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        logger.info(f"Signup attempt for email: {request.email}")
        
        # Check if user already exists
        from sqlalchemy import select
        result = await db.execute(select(User).where(User.email == request.email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.warning(f"User already exists: {request.email}")
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )

        logger.info(f"Creating new user: {request.email}")
        
        # Create new user
        user_id = uuid4()
        user = User(
            id=user_id,
            email=request.email,
            full_name=request.email.split('@')[0],  # Use email prefix as name
            created_at=datetime.utcnow()
        )
        db.add(user)

        # Create free subscription
        logger.info(f"Creating subscription for user: {user_id}")
        subscription = Subscription(
            user_id=user_id,  # UUID type
            tier=SubscriptionTier.FREE,
            started_at=datetime.utcnow()
        )
        db.add(subscription)

        logger.info("Committing to database...")
        await db.commit()
        logger.info(f"User created successfully: {user_id}")

        # Generate JWT tokens
        logger.info("Generating JWT tokens...")
        access_token = await create_access_token(
            data={"sub": str(user_id), "email": request.email}
        )
        refresh_token = await create_refresh_token(
            data={"sub": str(user_id)}
        )
        logger.info("Tokens generated successfully")

        return AuthResponse(
            success=True,
            message=f"Account created for {request.email}. Use the access_token for authenticated requests.",
            email=request.email,
            access_token=access_token,
            refresh_token=refresh_token
        )
    except HTTPException:
        logger.warning(f"HTTPException during signup")
        raise
    except Exception as e:
        logger.error(f"Error in signup: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Login user.
    
    For Phase 1 testing: Returns JWT token.
    In production: Would use Supabase Auth magic links.
    """
    # Check if user exists
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found. Please sign up first."
        )
    
    # Generate JWT tokens
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id}
    )
    
    return AuthResponse(
        success=True,
        message=f"Welcome back, {user.email}!",
        email=request.email,
        access_token=access_token,
        refresh_token=refresh_token
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
