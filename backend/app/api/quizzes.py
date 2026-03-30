"""
Quizzes API Router

Endpoints for quiz retrieval, submission, and grading.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import uuid
import random

from app.database import get_db
from app.models.chapter import Chapter
from app.models.progress import QuizQuestion, QuizAttempt
from app.models.user import Subscription, SubscriptionTier
from app.schemas.chapter import (
    QuizResponse,
    QuizData,
    QuizQuestion as QuizQuestionSchema,
    QuizOption,
    QuizSubmitRequest,
    QuizSubmitResponse,
    QuizResult,
    GradedAnswer,
    QuizHistoryResponse,
    QuizHistoryData,
    QuizAttemptSummary,
    ERROR_CODES
)
from app.api.chapters import get_current_user

router = APIRouter(prefix="/chapters", tags=["Quizzes"])


@router.get("/{chapter_id}/quiz", response_model=QuizResponse)
async def get_quiz(
    chapter_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get quiz for a chapter.
    
    Randomly selects 5 questions from the question bank.
    """
    # Verify chapter exists
    chapter_result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    chapter = chapter_result.scalar_one_or_none()
    
    if not chapter:
        raise HTTPException(
            status_code=404,
            detail=ERROR_CODES["CHAPTER_NOT_FOUND"]["message"]
        )
    
    # Get all questions for this chapter
    questions_result = await db.execute(
        select(QuizQuestion)
        .where(QuizQuestion.chapter_id == chapter_id)
        .order_by(QuizQuestion.order_in_chapter)
    )
    all_questions = questions_result.scalars().all()
    
    if not all_questions:
        raise HTTPException(
            status_code=404,
            detail=ERROR_CODES["QUIZ_NOT_FOUND"]["message"]
        )
    
    # Randomly select 5 questions (or all if less than 5)
    selected_questions = random.sample(all_questions, min(5, len(all_questions)))
    
    # Build quiz questions (without correct answers)
    quiz_questions = []
    for idx, q in enumerate(selected_questions):
        import json
        options_dict = json.loads(q.options_json)
        options = [
            QuizOption(id=opt_id, text=opt_text)
            for opt_id, opt_text in options_dict.items()
        ]
        quiz_questions.append(QuizQuestionSchema(
            question_id=q.id,
            question_text=q.question_text,
            options=options,
            question_number=idx + 1
        ))
    
    # Generate unique quiz session ID
    quiz_session_id = f"quiz-{chapter_id}-{uuid.uuid4().hex[:8]}"
    
    return QuizResponse(
        success=True,
        data=QuizData(
            quiz_id=quiz_session_id,
            chapter_id=chapter_id,
            chapter_title=chapter.title,
            total_questions=len(quiz_questions),
            passing_score=80,
            questions=quiz_questions
        )
    )


@router.post("/quizzes/{quiz_id}/submit", response_model=QuizSubmitResponse)
async def submit_quiz(
    quiz_id: str,
    request: QuizSubmitRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Submit quiz answers for grading.
    
    Grades answers using answer key and records attempt.
    """
    # Extract chapter_id from quiz_id (format: quiz-{chapter_id}-{session})
    try:
        chapter_id = int(quiz_id.split("-")[1])
    except (IndexError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid quiz ID format"
        )
    
    # Get all questions and correct answers
    questions_result = await db.execute(
        select(QuizQuestion).where(QuizQuestion.chapter_id == chapter_id)
    )
    all_questions = {q.id: q for q in questions_result.scalars().all()}
    
    if not all_questions:
        raise HTTPException(
            status_code=404,
            detail=ERROR_CODES["QUIZ_NOT_FOUND"]["message"]
        )
    
    # Grade answers
    graded_answers = []
    correct_count = 0
    
    for answer in request.answers:
        question = all_questions.get(answer.question_id)
        if not question:
            raise HTTPException(
                status_code=400,
                detail=f"Question {answer.question_id} not found"
            )
        
        is_correct = answer.answer == question.correct_answer
        if is_correct:
            correct_count += 1
        
        graded_answers.append(GradedAnswer(
            question_id=answer.question_id,
            question_text=question.question_text,
            student_answer=answer.answer,
            correct_answer=question.correct_answer,
            is_correct=is_correct,
            explanation=question.explanation or "",
            why_wrong=question.why_wrong,
            source_reference=question.source_reference or f"Chapter {chapter_id}"
        ))
    
    # Calculate score
    total_questions = len(request.answers)
    score = int((correct_count / total_questions) * 100) if total_questions > 0 else 0
    passed = score >= 80
    
    # Get attempt number
    attempt_result = await db.execute(
        select(QuizAttempt)
        .where(QuizAttempt.user_id == current_user['user_id'])
        .where(QuizAttempt.chapter_id == chapter_id)
        .order_by(QuizAttempt.attempt_number.desc())
        .limit(1)
    )
    last_attempt = attempt_result.scalar_one_or_none()
    attempt_number = (last_attempt.attempt_number + 1) if last_attempt else 1
    
    # Record attempt
    quiz_attempt = QuizAttempt(
        user_id=current_user['user_id'],
        chapter_id=chapter_id,
        quiz_session_id=quiz_id,
        score=score,
        total_questions=total_questions,
        correct_answers=correct_count,
        incorrect_answers=total_questions - correct_count,
        passed=passed,
        passing_score=80,
        answers=[
            {
                "question_id": ga.question_id,
                "answer": ga.student_answer,
                "is_correct": ga.is_correct
            }
            for ga in graded_answers
        ],
        attempt_number=attempt_number
    )
    db.add(quiz_attempt)
    await db.commit()
    
    # Generate feedback
    feedback = {
        "overall": f"{'Great job! You passed!' if passed else 'Keep studying! You can retake this quiz.'}",
        "recommendation": "Review the chapter content for better understanding." if not passed else "Ready for the next chapter!"
    }
    
    next_steps = {
        "retake_allowed": True,
        "next_chapter_available": passed,
        "recommended_action": "continue" if passed else "review"
    }
    
    return QuizSubmitResponse(
        success=True,
        data=QuizResult(
            quiz_id=quiz_id,
            chapter_id=chapter_id,
            user_id=current_user['user_id'],
            score=score,
            total_questions=total_questions,
            correct_answers=correct_count,
            incorrect_answers=total_questions - correct_count,
            passed=passed,
            passing_score=80,
            submitted_at=datetime.utcnow(),
            time_taken_seconds=None,
            attempt_number=attempt_number,
            answers=graded_answers,
            feedback=feedback,
            next_steps=next_steps
        )
    )


@router.get("/{chapter_id}/quiz/history", response_model=QuizHistoryResponse)
async def get_quiz_history(
    chapter_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get quiz attempt history for a chapter.
    """
    # Get chapter
    chapter_result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    chapter = chapter_result.scalar_one_or_none()
    
    if not chapter:
        raise HTTPException(
            status_code=404,
            detail=ERROR_CODES["CHAPTER_NOT_FOUND"]["message"]
        )
    
    # Get all attempts
    attempts_result = await db.execute(
        select(QuizAttempt)
        .where(QuizAttempt.user_id == current_user['user_id'])
        .where(QuizAttempt.chapter_id == chapter_id)
        .order_by(QuizAttempt.submitted_at.desc())
    )
    attempts = attempts_result.scalars().all()
    
    if not attempts:
        return QuizHistoryResponse(
            success=True,
            data=QuizHistoryData(
                chapter_id=chapter_id,
                chapter_title=chapter.title,
                total_attempts=0,
                best_score=0,
                latest_score=0,
                average_score=0.0,
                passed=False,
                attempts=[]
            )
        )
    
    # Calculate statistics
    scores = [a.score for a in attempts]
    best_score = max(scores)
    latest_score = attempts[0].score if attempts else 0
    average_score = sum(scores) / len(scores) if scores else 0.0
    passed = any(a.passed for a in attempts)
    
    # Format attempts
    attempt_summaries = [
        QuizAttemptSummary(
            quiz_id=a.quiz_session_id,
            score=a.score,
            passed=a.passed,
            attempt_number=a.attempt_number,
            submitted_at=a.submitted_at,
            time_taken_seconds=a.time_taken_seconds
        )
        for a in attempts
    ]
    
    return QuizHistoryResponse(
        success=True,
        data=QuizHistoryData(
            chapter_id=chapter_id,
            chapter_title=chapter.title,
            total_attempts=len(attempts),
            best_score=best_score,
            latest_score=latest_score,
            average_score=average_score,
            passed=passed,
            attempts=attempt_summaries
        )
    )
