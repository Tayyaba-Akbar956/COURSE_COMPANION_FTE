"""
Progress API Router

Endpoints for tracking and retrieving user progress.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta
import uuid

from app.database import get_db
from app.models.chapter import Chapter
from app.models.progress import ChapterProgress, QuizAttempt
from app.models.achievement import DailyStreak, Achievement, UserAchievement
from app.models.user import Subscription, SubscriptionTier
from app.schemas.chapter import (
    ProgressResponse,
    ProgressData,
    OverallProgress,
    StreakInfo,
    ModuleProgress,
    AchievementInfo,
    ProgressUpdateRequest,
    ProgressUpdateResponse,
    ProgressUpdateData,
    ERROR_CODES
)
from app.api.chapters import get_current_user

router = APIRouter(prefix="/users", tags=["Progress"])


@router.get("/{user_id}/progress", response_model=ProgressResponse)
async def get_progress(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get comprehensive progress for a user.
    
    Returns chapters completed, streaks, achievements, and module progress.
    """
    # Verify user can only access own progress
    if user_id != current_user['user_id']:
        raise HTTPException(
            status_code=403,
            detail=ERROR_CODES["ACCESS_DENIED"]["message"]
        )
    
    # Get total chapters
    total_chapters_result = await db.execute(select(func.count(Chapter.id)))
    total_chapters = total_chapters_result.scalar() or 0
    
    # Get user's completed chapters
    completed_result = await db.execute(
        select(ChapterProgress)
        .where(ChapterProgress.user_id == user_id)
        .where(ChapterProgress.completed == True)
    )
    completed = completed_result.scalars().all()
    chapters_completed = len(completed)
    
    # Get quiz attempts
    quiz_result = await db.execute(
        select(QuizAttempt)
        .where(QuizAttempt.user_id == user_id)
    )
    quiz_attempts = quiz_result.scalars().all()
    quizzes_completed = len(quiz_attempts)
    
    # Calculate average quiz score
    average_quiz_score = None
    if quiz_attempts:
        scores = [q.score for q in quiz_attempts]
        average_quiz_score = sum(scores) / len(scores)
    
    # Calculate total time spent
    total_time_seconds = sum(cp.time_spent_seconds for cp in completed)
    time_spent_minutes = int(total_time_seconds / 60)
    
    # Get current streak
    today = datetime.utcnow().date()
    streak_result = await db.execute(
        select(DailyStreak)
        .where(DailyStreak.user_id == user_id)
        .order_by(DailyStreak.activity_date.desc())
    )
    all_streaks = streak_result.scalars().all()
    
    current_streak = 0
    longest_streak = 0
    
    if all_streaks:
        # Calculate current streak
        last_activity = all_streaks[0].activity_date.date()
        if last_activity == today or last_activity == today - timedelta(days=1):
            current_streak = 1
            for i in range(1, len(all_streaks)):
                prev_date = all_streaks[i-1].activity_date.date()
                curr_date = all_streaks[i].activity_date.date()
                if (prev_date - curr_date).days == 1:
                    current_streak += 1
                else:
                    break
        
        # Calculate longest streak
        longest_streak = max(len(all_streaks), current_streak)
    
    # Get module progress
    modules_result = await db.execute(
        select(Chapter.module_id, func.count(Chapter.id))
        .group_by(Chapter.module_id)
    )
    module_totals = dict(modules_result.all())
    
    module_progress_list = []
    for module_id, total in module_totals.items():
        completed_in_module = await db.execute(
            select(func.count(ChapterProgress.id))
            .where(ChapterProgress.user_id == user_id)
            .where(ChapterProgress.completed == True)
            .join(Chapter, ChapterProgress.chapter_id == Chapter.id)
            .where(Chapter.module_id == module_id)
        )
        completed_count = completed_in_module.scalar() or 0
        
        module_progress_list.append(ModuleProgress(
            module_id=module_id,
            module_title=f"Module {module_id}",
            chapters_completed=completed_count,
            total_chapters=total,
            completion_percentage=(completed_count / total * 100) if total > 0 else 0
        ))
    
    # Get achievements
    all_achievements_result = await db.execute(
        select(Achievement).where(Achievement.is_active == True)
    )
    all_achievements = all_achievements_result.scalars().all()
    
    user_achievements_result = await db.execute(
        select(UserAchievement).where(UserAchievement.user_id == user_id)
    )
    user_achievement_ids = {ua.achievement_id for ua in user_achievements_result.scalars().all()}
    
    earned = []
    locked = []
    for achievement in all_achievements:
        achievement_info = AchievementInfo(
            achievement_id=achievement.id,
            name=achievement.name,
            description=achievement.description,
            icon=achievement.icon,
            unlocked_at=None
        )
        
        if achievement.id in user_achievement_ids:
            earned.append(achievement_info)
        else:
            locked.append(achievement_info)
    
    # Calculate completion percentage
    completion_percentage = (chapters_completed / total_chapters * 100) if total_chapters > 0 else 0
    
    return ProgressResponse(
        success=True,
        data=ProgressData(
            user_id=user_id,
            overall_progress=OverallProgress(
                chapters_completed=chapters_completed,
                total_chapters=total_chapters,
                completion_percentage=completion_percentage,
                quizzes_completed=quizzes_completed,
                average_quiz_score=average_quiz_score,
                time_spent_minutes=time_spent_minutes
            ),
            streak=StreakInfo(
                current_streak=current_streak,
                longest_streak=longest_streak,
                streak_active=current_streak > 0
            ),
            module_progress=module_progress_list,
            achievements={
                "earned": earned,
                "locked": locked
            }
        )
    )


@router.put("/{user_id}/progress", response_model=ProgressUpdateResponse)
async def update_progress(
    user_id: str,
    request: ProgressUpdateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update user progress (mark chapter as complete/in-progress/start).
    """
    # Verify user can only update own progress
    if user_id != current_user['user_id']:
        raise HTTPException(
            status_code=403,
            detail=ERROR_CODES["ACCESS_DENIED"]["message"]
        )
    
    # Verify chapter exists
    chapter_result = await db.execute(select(Chapter).where(Chapter.id == request.chapter_id))
    chapter = chapter_result.scalar_one_or_none()
    
    if not chapter:
        raise HTTPException(
            status_code=404,
            detail=ERROR_CODES["CHAPTER_NOT_FOUND"]["message"]
        )
    
    # Get or create progress
    progress_result = await db.execute(
        select(ChapterProgress)
        .where(ChapterProgress.user_id == user_id)
        .where(ChapterProgress.chapter_id == request.chapter_id)
    )
    progress = progress_result.scalar_one_or_none()
    
    if not progress:
        progress = ChapterProgress(
            user_id=user_id,
            chapter_id=request.chapter_id
        )
        db.add(progress)
    
    # Update based on action
    if request.action == "complete":
        progress.completed = True
        progress.completed_at = datetime.utcnow()
        if request.time_spent_seconds:
            progress.time_spent_seconds = request.time_spent_seconds
    elif request.action == "in_progress":
        progress.completed = False
        progress.last_accessed_at = datetime.utcnow()
    elif request.action == "start":
        progress.last_accessed_at = datetime.utcnow()
    
    await db.commit()
    
    # Check for achievements (simplified)
    achievements_unlocked = []
    if request.chapter_id == 1 and request.action == "complete":
        achievements_unlocked.append(AchievementInfo(
            achievement_id="first_chapter",
            name="First Steps",
            description="Complete your first chapter",
            icon="🏅",
            unlocked_at=datetime.utcnow()
        ))
    
    # Recalculate overall progress
    completed_result = await db.execute(
        select(ChapterProgress)
        .where(ChapterProgress.user_id == user_id)
        .where(ChapterProgress.completed == True)
    )
    completed_count = len(completed_result.scalars().all())
    
    total_chapters_result = await db.execute(select(func.count(Chapter.id)))
    total_chapters = total_chapters_result.scalar() or 0
    
    completion_percentage = (completed_count / total_chapters * 100) if total_chapters > 0 else 0
    
    return ProgressUpdateResponse(
        success=True,
        data=ProgressUpdateData(
            chapter_id=request.chapter_id,
            completed=progress.completed,
            achievements_unlocked=achievements_unlocked,
            streak_updated={"current_streak": 1, "streak_maintained": True},
            new_overall_progress=OverallProgress(
                chapters_completed=completed_count,
                total_chapters=total_chapters,
                completion_percentage=completion_percentage,
                quizzes_completed=0,
                average_quiz_score=None,
                time_spent_minutes=0
            )
        )
    )
