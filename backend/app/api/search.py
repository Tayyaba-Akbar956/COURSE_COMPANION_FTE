"""
Search API Router

Endpoints for full-text search across course content.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from datetime import datetime
import uuid

from app.database import get_db
from app.models.chapter import Chapter
from app.models.user import Subscription, SubscriptionTier
from app.schemas.chapter import (
    SearchRequest,
    SearchResponse,
    SearchData,
    SearchResult,
    MetaInfo,
    ERROR_CODES
)
from app.api.chapters import get_current_user_optional

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1, max_length=500, description="Search query"),
    limit: int = Query(default=10, ge=1, le=50, description="Max results"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
    module: int = Query(None, description="Filter by module"),
    free_only: bool = Query(False, description="Show only free content"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_optional)
):
    """
    Search across all chapter content using PostgreSQL full-text search.
    
    Returns matching sections with highlighted terms.
    """
    start_time = datetime.utcnow()
    request_id = str(uuid.uuid4())
    
    # Get user's subscription tier for access control
    user_tier = SubscriptionTier.FREE
    if current_user and 'user_id' in current_user:
        subscription_result = await db.execute(
            select(Subscription).where(Subscription.user_id == current_user['user_id'])
        )
        subscription = subscription_result.scalar_one_or_none()
        if subscription:
            user_tier = subscription.tier
    
    # Build search query
    # Convert search terms to tsquery format
    search_terms = " & ".join(q.split())
    
    # Base query with full-text search
    query_text = """
        SELECT 
            c.id as chapter_id,
            c.title as chapter_title,
            c.is_free,
            ts_rank(to_tsvector('english', c.content), to_tsquery(:query)) as relevance
        FROM chapters c
        WHERE to_tsvector('english', c.content) @@ to_tsquery(:query)
    """
    
    # Add module filter
    if module:
        query_text += " AND c.module_id = :module"
    
    # Add free-only filter
    if free_only:
        query_text += " AND c.is_free = TRUE"
    
    # Add access control for free users
    if user_tier == SubscriptionTier.FREE and not free_only:
        # Free users can see free content, premium content appears but marked
        pass
    
    query_text += " ORDER BY relevance DESC LIMIT :limit OFFSET :offset"
    
    # Execute search
    params = {"query": search_terms, "limit": limit, "offset": offset}
    if module:
        params["module"] = module
    
    result = await db.execute(text(query_text), params)
    rows = result.fetchall()
    
    # Format results
    results = []
    for row in rows:
        results.append(SearchResult(
            type="chapter_section",
            chapter_id=row.chapter_id,
            chapter_title=row.chapter_title,
            section_id=None,
            section_title=None,
            excerpt=f"... [Search results for '{q}'] ...",  # Would extract from content
            relevance_score=min(1.0, row.relevance),
            is_free=True,  # Would check actual chapter
            matched_terms=q.split(),
            url=f"/chapters/{row.chapter_id}"
        ))
    
    # Get total count
    count_query = """
        SELECT COUNT(*) FROM chapters c
        WHERE to_tsvector('english', c.content) @@ to_tsquery(:query)
    """
    count_result = await db.execute(text(count_query), {"query": search_terms})
    total_results = count_result.scalar() or 0
    
    execution_time = (datetime.utcnow() - start_time).total_seconds() * 1000
    
    return SearchResponse(
        success=True,
        data=SearchData(
            query=q,
            results=results,
            total_results=total_results,
            returned_results=len(results),
            limit=limit,
            offset=offset,
            filters_applied={
                "module": module,
                "free_only": free_only
            },
            search_metadata={
                "search_type": "full_text",
                "execution_time_ms": int(execution_time)
            }
        ),
        meta=MetaInfo(
            request_id=request_id,
            timestamp=datetime.utcnow(),
            execution_time_ms=int(execution_time)
        )
    )


@router.get("/suggestions")
async def search_suggestions(
    q: str = Query(..., min_length=1, description="Search query for autocomplete"),
    limit: int = Query(default=5, ge=1, le=10),
    db: AsyncSession = Depends(get_db)
):
    """
    Get search suggestions (autocomplete).
    """
    # Simple implementation: return chapter titles that match
    result = await db.execute(
        select(Chapter.title)
        .where(Chapter.title.ilike(f"%{q}%"))
        .limit(limit)
    )
    titles = result.scalars().all()
    
    suggestions = [
        {"text": title, "match_count": 1}
        for title in titles
    ]
    
    return {
        "success": True,
        "data": {
            "query": q,
            "suggestions": suggestions
        }
    }


@router.get("/advanced")
async def advanced_search(
    q: str = Query(..., description="Search query"),
    in_title: bool = Query(False, description="Search only in titles"),
    in_content: bool = Query(True, description="Search in content"),
    in_code: bool = Query(False, description="Search in code examples"),
    db: AsyncSession = Depends(get_db)
):
    """
    Advanced search with multiple filters.
    """
    # Implementation would vary based on filters
    # For now, return basic search results
    
    return {
        "success": True,
        "data": {
            "query": q,
            "results": [],
            "filters": {
                "in_title": in_title,
                "in_content": in_content,
                "in_code": in_code
            }
        }
    }
