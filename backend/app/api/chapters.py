"""
Chapters API Router

Endpoints for listing and retrieving course chapters.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
import uuid

from app.database import get_db
from app.models.chapter import Chapter as ChapterModel, Module
from app.models.user import Subscription, SubscriptionTier
from app.schemas.chapter import (
    ChapterListResponse,
    ChapterListData,
    ChapterListItem,
    Chapter as ChapterSchema,
    MetaInfo,
    ChapterCompleteRequest,
    ChapterCompleteResponse,
    ChapterCompleteData,
    ERROR_CODES
)
from app.security import verify_token

router = APIRouter(prefix="/chapters", tags=["Chapters"])


# =============================================================================
# Dependencies
# =============================================================================

async def get_current_user_optional(request: Request) -> Optional[dict]:
    """
    Get current user if authenticated, None otherwise.
    
    Used for endpoints that work for both authenticated and anonymous users.
    """
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        token = auth_header.replace("Bearer ", "")
        payload = await verify_token(token)
        return payload
    except:
        return None


async def get_current_user(request: Request) -> dict:
    """
    Get current user (required).
    
    Raises 401 if not authenticated.
    """
    user = await get_current_user_optional(request)
    if not user:
        raise HTTPException(
            status_code=401,
            detail=ERROR_CODES["UNAUTHORIZED"]["message"]
        )
    return user


# =============================================================================
# API Endpoints
# =============================================================================

@router.get("", response_model=ChapterListResponse)
async def list_chapters(
    module: Optional[int] = Query(None, description="Filter by module ID"),
    include_progress: bool = Query(False, description="Include user progress"),
    free_only: bool = Query(False, description="Show only free chapters"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    List all chapters with optional filtering.

    - **module**: Filter by module ID
    - **include_progress**: Include user's completion status
    - **free_only**: Show only free chapters
    """
    start_time = datetime.utcnow()
    request_id = str(uuid.uuid4())

    try:
        # Build query
        from sqlalchemy import select
        query = select(ChapterModel).join(Module).order_by(Module.module_order, ChapterModel.order_in_module)

        # Apply filters
        if module:
            query = query.where(ChapterModel.module_id == module)

        if free_only:
            query = query.where(ChapterModel.is_free == True)

        # Execute query
        result = await db.execute(query)
        chapters = result.scalars().all()

        # Get user's subscription tier if authenticated
        user_tier = SubscriptionTier.FREE
        if current_user and 'user_id' in current_user:
            from sqlalchemy import select as async_select
            subscription_result = await db.execute(
                async_select(Subscription).where(Subscription.user_id == current_user['user_id'])
            )
            subscription = subscription_result.scalar_one_or_none()
            if subscription:
                user_tier = subscription.tier

        # Convert to response format
        chapter_items = []
        for chapter in chapters:
            # Get module title safely
            module_title = "Unknown"
            if hasattr(chapter, 'module') and chapter.module:
                module_title = chapter.module.title
            
            chapter_items.append(ChapterListItem(
                id=chapter.id,
                chapter_number=chapter.chapter_number,
                module_id=chapter.module_id,
                module_title=module_title,
                title=chapter.title,
                is_free=chapter.is_free,
                estimated_minutes=chapter.estimated_minutes,
                order_in_module=chapter.order_in_module,
                quiz_available=True  # All chapters have quizzes
            ))

        execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000

        return ChapterListResponse(
            success=True,
            data=ChapterListData(
                chapters=chapter_items,
                total_chapters=len(chapter_items),
                returned_chapters=len(chapter_items),
                filters_applied={
                    "module": module,
                    "include_progress": include_progress,
                    "free_only": free_only
                }
            ),
            meta=MetaInfo(
                request_id=request_id,
                timestamp=datetime.utcnow(),
                execution_time_ms=int(execution_time)
            )
        )
    except Exception as e:
        # Log the actual error for debugging
        import logging
        logging.error(f"Error in list_chapters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/{chapter_id}", response_model=dict)
async def get_chapter(
    chapter_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional)
):
    """
    Get full chapter content by ID.
    
    Returns chapter content, sections, images, code examples, and navigation links.
    """
    from sqlalchemy import select
    
    # Get chapter with module
    result = await db.execute(
        select(ChapterModel).join(Module).where(ChapterModel.id == chapter_id)
    )
    chapter = result.scalar_one_or_none()
    
    if not chapter:
        raise HTTPException(
            status_code=404,
            detail=ERROR_CODES["CHAPTER_NOT_FOUND"]["message"]
        )
    
    # Check access
    if not chapter.is_free:
        if not current_user or 'user_id' not in current_user:
            raise HTTPException(
                status_code=403,
                detail="Authentication required for premium content"
            )
        
        # Check subscription
        from sqlalchemy import select as async_select
        subscription_result = await db.execute(
            async_select(Subscription).where(Subscription.user_id == current_user['user_id'])
        )
        subscription = subscription_result.scalar_one_or_none()
        
        if not subscription or subscription.tier == SubscriptionTier.FREE:
            raise HTTPException(
                status_code=403,
                detail="This chapter requires premium access"
            )
    
    # Get navigation
    prev_result = await db.execute(
        select(ChapterModel).where(ChapterModel.order_in_module < chapter.order_in_module)
        .where(ChapterModel.module_id == chapter.module_id)
        .order_by(ChapterModel.order_in_module.desc())
        .limit(1)
    )
    prev_chapter = prev_result.scalar_one_or_none()
    
    next_result = await db.execute(
        select(ChapterModel).where(ChapterModel.order_in_module > chapter.order_in_module)
        .where(ChapterModel.module_id == chapter.module_id)
        .order_by(ChapterModel.order_in_module.asc())
        .limit(1)
    )
    next_chapter = next_result.scalar_one_or_none()
    
    # Build response
    chapter_data = {
        "id": chapter.id,
        "chapter_number": chapter.chapter_number,
        "module_id": chapter.module_id,
        "module_title": chapter.module.title if chapter.module else "Unknown",
        "title": chapter.title,
        "content": chapter.content,
        "content_html": chapter.content_html,
        "is_free": chapter.is_free,
        "estimated_minutes": chapter.estimated_minutes,
        "order_in_module": chapter.order_in_module,
        "sections": [],  # Would parse from content
        "images": [],    # Would load from R2
        "code_examples": [],  # Would parse from content
        "navigation": {
            "previous_chapter_id": prev_chapter.id if prev_chapter else None,
            "next_chapter_id": next_chapter.id if next_chapter else None,
            "previous_chapter_title": prev_chapter.title if prev_chapter else None,
            "next_chapter_title": next_chapter.title if next_chapter else None
        },
        "quiz": {
            "available": True,
            "quiz_id": chapter.id,  # Quiz ID matches chapter ID
            "total_questions": 5,
            "passing_score": 80
        },
        "created_at": chapter.created_at,
        "updated_at": chapter.updated_at
    }
    
    return {"success": True, "data": {"chapter": chapter_data}}


@router.post("/{chapter_id}/complete", response_model=ChapterCompleteResponse)
async def complete_chapter(
    chapter_id: int,
    request: ChapterCompleteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Mark a chapter as completed.
    
    Tracks completion time and unlocks achievements.
    """
    from sqlalchemy import select
    from app.models.progress import ChapterProgress
    
    # Verify chapter exists
    from sqlalchemy import select as async_select
    chapter_result = await db.execute(async_select(ChapterModel).where(ChapterModel.id == chapter_id))
    chapter = chapter_result.scalar_one_or_none()
    
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    # Get or create progress
    progress_result = await db.execute(
        select(ChapterProgress).where(
            ChapterProgress.user_id == current_user['user_id'],
            ChapterProgress.chapter_id == chapter_id
        )
    )
    progress = progress_result.scalar_one_or_none()
    
    if not progress:
        progress = ChapterProgress(
            user_id=current_user['user_id'],
            chapter_id=chapter_id,
            completed=True,
            completed_at=datetime.utcnow(),
            time_spent_seconds=request.time_spent_seconds or 0
        )
        db.add(progress)
    else:
        progress.completed = True
        progress.completed_at = datetime.utcnow()
        if request.time_spent_seconds:
            progress.time_spent_seconds = request.time_spent_seconds
    
    await db.commit()
    
    # Check for achievements (simplified)
    achievements_unlocked = []
    if chapter_id == 1:  # First chapter
        achievements_unlocked.append({
            "achievement_id": "first_chapter",
            "name": "First Steps",
            "icon": "🏅"
        })
    
    return ChapterCompleteResponse(
        success=True,
        data=ChapterCompleteData(
            chapter_id=chapter_id,
            completed=True,
            completed_at=datetime.utcnow(),
            time_spent_seconds=request.time_spent_seconds,
            achievements_unlocked=achievements_unlocked
        )
    )
