from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.user import User
from backend.models.assessment import AssessmentQuestion, AssessmentSubmission, AssessmentAnswer
from backend.models.progress import StudentProgress
from backend.schemas import (
    QuestionOptionResponse,
    AssessmentSubmitRequest,
    AssessmentSubmissionResponse,
    KnowledgeGapItem
)
from backend.services.auth import get_current_user
from backend.services.recommender import recommender_engine, CANONICAL_SKILLS

router = APIRouter(prefix="/assessment", tags=["Assessment"])

@router.get("/questions", response_model=List[QuestionOptionResponse])
def get_assessment_questions(db: Session = Depends(get_db)):
    questions = db.query(AssessmentQuestion).all()
    # Format questions cleanly without exposing correct_option_index
    return [
        QuestionOptionResponse(
            id=q.id,
            question_text=q.question_text,
            skill_code=q.skill_code,
            options=q.options,
            difficulty=q.difficulty,
            topic=q.topic
        )
        for q in questions
    ]

@router.post("/submit", response_model=AssessmentSubmissionResponse)
def submit_assessment(
    submission_data: AssessmentSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not submission_data.answers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment submission contains no answers."
        )

    # Fetch all questions
    question_ids = [a.question_id for a in submission_data.answers]
    questions_db = db.query(AssessmentQuestion).filter(AssessmentQuestion.id.in_(question_ids)).all()
    question_map = {q.id: q for q in questions_db}

    # Evaluate
    skill_stats = {s: {"total": 0, "correct": 0} for s in CANONICAL_SKILLS}
    missed_topics = []
    answers_to_save = []

    for user_ans in submission_data.answers:
        q = question_map.get(user_ans.question_id)
        if not q:
            continue

        skill_code = q.skill_code
        if skill_code not in skill_stats:
            skill_stats[skill_code] = {"total": 0, "correct": 0}

        skill_stats[skill_code]["total"] += 1
        is_correct = 1 if user_ans.selected_option == q.correct_option_index else 0
        if is_correct:
            skill_stats[skill_code]["correct"] += 1
        else:
            missed_topics.append({
                "skill_code": skill_code,
                "topic": q.topic or f"{skill_code.title()} Fundamentals",
                "explanation": q.explanation
            })

        answers_to_save.append({
            "question_id": q.id,
            "selected_option": user_ans.selected_option,
            "is_correct": is_correct
        })

    # Calculate skill scores
    skill_scores = {}
    for s, stats in skill_stats.items():
        if stats["total"] > 0:
            skill_scores[s] = round((stats["correct"] / stats["total"]) * 100.0, 1)
        else:
            skill_scores[s] = 0.0

    total_correct = sum(stats["correct"] for stats in skill_stats.values())
    total_q = sum(stats["total"] for stats in skill_stats.values())
    overall_score = round((total_correct / max(total_q, 1)) * 100.0, 1)

    # Use Recommender Engine to identify gaps
    identified_gaps = recommender_engine.identify_gaps(skill_scores, missed_topics)

    # Save submission
    submission = AssessmentSubmission(
        user_id=current_user.id,
        total_score=overall_score,
        skill_scores=skill_scores,
        knowledge_gaps=identified_gaps
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    for ans in answers_to_save:
        db.add(AssessmentAnswer(
            submission_id=submission.id,
            question_id=ans["question_id"],
            selected_option=ans["selected_option"],
            is_correct=ans["is_correct"]
        ))

    # Update StudentProgress for each skill
    for code, score in skill_scores.items():
        prog = db.query(StudentProgress).filter(
            StudentProgress.user_id == current_user.id,
            StudentProgress.skill_code == code
        ).first()

        level = "Master" if score >= 85 else ("Advanced" if score >= 70 else ("Intermediate" if score >= 40 else "Novice"))
        if not prog:
            prog = StudentProgress(
                user_id=current_user.id,
                skill_code=code,
                proficiency_score=score,
                proficiency_level=level
            )
            db.add(prog)
        else:
            prog.proficiency_score = score
            prog.proficiency_level = level

    db.commit()

    gap_items = [
        KnowledgeGapItem(
            skill_code=g["skill_code"],
            topic=g["topic"],
            severity=g["severity"],
            recommendation=g["recommendation"]
        )
        for g in identified_gaps
    ]

    return AssessmentSubmissionResponse(
        id=submission.id,
        user_id=submission.user_id,
        total_score=submission.total_score,
        skill_scores=submission.skill_scores,
        knowledge_gaps=gap_items,
        submitted_at=submission.submitted_at
    )
