from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from backend.database import get_db
from backend.models.user import User
from backend.models.profile import StudentProfile
from backend.models.assessment import AssessmentSubmission
from backend.models.pathway import LearningPathway, PathwayStep
from backend.models.resource import LearningResource
from backend.models.progress import StudentProgress
from backend.schemas import PathwayGenerateRequest, PathwayResponse, PathwayStepResponse
from backend.services.auth import get_current_user
from backend.services.recommender import recommender_engine

router = APIRouter(prefix="/pathways", tags=["Pathways"])

@router.post("/generate", response_model=PathwayResponse)
def generate_student_pathway(
    req: PathwayGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    career_goal = req.career_goal or (profile.career_goal if profile else "Full-Stack Web Developer")
    daily_hours = req.daily_study_hours or (profile.daily_study_hours if profile else 2.0)
    target_date = req.target_date or (profile.target_date if profile else None)

    # Fetch latest assessment
    latest_sub = db.query(AssessmentSubmission).filter(
        AssessmentSubmission.user_id == current_user.id
    ).order_by(AssessmentSubmission.submitted_at.desc()).first()

    skill_scores = latest_sub.skill_scores if latest_sub else {"python": 50, "sql": 40, "web_dev": 40}
    gaps = latest_sub.knowledge_gaps if latest_sub else []

    # Fetch resources
    all_res = db.query(LearningResource).all()
    res_dicts = [
        {
            "id": r.id,
            "title": r.title,
            "skill_code": r.skill_code,
            "category": r.category,
            "url": r.url,
            "is_free": r.is_free,
            "difficulty": r.difficulty,
            "provider": r.provider,
            "description": r.description
        }
        for r in all_res
    ]

    # Generate via scikit-learn recommendation engine
    generated = recommender_engine.generate_pathway(
        career_goal=career_goal,
        skill_scores=skill_scores,
        gaps=gaps,
        daily_study_hours=daily_hours,
        resources_catalog=res_dicts
    )

    # Archive previous active pathways
    existing_pathways = db.query(LearningPathway).filter(
        LearningPathway.user_id == current_user.id,
        LearningPathway.status == "active"
    ).all()
    for ep in existing_pathways:
        ep.status = "archived"

    # Create new active pathway
    pathway = LearningPathway(
        user_id=current_user.id,
        career_goal=career_goal,
        title=generated["title"],
        description=generated["description"],
        target_date=target_date,
        total_duration_weeks=generated["total_duration_weeks"],
        progress_percentage=0.0,
        status="active"
    )
    db.add(pathway)
    db.commit()
    db.refresh(pathway)

    # Add steps
    created_steps = []
    for s_data in generated["steps"]:
        step = PathwayStep(
            pathway_id=pathway.id,
            order_index=s_data["order_index"],
            skill_code=s_data["skill_code"],
            stage_name=s_data["stage_name"],
            title=s_data["title"],
            description=s_data["description"],
            duration_hours=s_data["duration_hours"],
            learning_objectives=s_data["learning_objectives"],
            resources=s_data["resources"],
            quiz_data=s_data["quiz_data"],
            practical_tasks=s_data["practical_tasks"],
            is_completed=False
        )
        db.add(step)
        created_steps.append(step)

    db.commit()
    db.refresh(pathway)

    # Format response
    steps_resp = [PathwayStepResponse.model_validate(st) for st in created_steps]
    resp = PathwayResponse.model_validate(pathway)
    resp.steps = steps_resp
    return resp

@router.get("/me", response_model=PathwayResponse)
def get_current_pathway(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    pathway = db.query(LearningPathway).filter(
        LearningPathway.user_id == current_user.id,
        LearningPathway.status == "active"
    ).order_by(LearningPathway.generated_at.desc()).first()

    if not pathway:
        # Auto-generate if no active pathway exists
        return generate_student_pathway(PathwayGenerateRequest(), current_user, db)

    steps = db.query(PathwayStep).filter(
        PathwayStep.pathway_id == pathway.id
    ).order_by(PathwayStep.order_index).all()

    steps_resp = [PathwayStepResponse.model_validate(st) for st in steps]
    resp = PathwayResponse.model_validate(pathway)
    resp.steps = steps_resp
    return resp

@router.post("/steps/{step_id}/toggle", response_model=PathwayResponse)
def toggle_step_completion(
    step_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    step = db.query(PathwayStep).join(LearningPathway).filter(
        PathwayStep.id == step_id,
        LearningPathway.user_id == current_user.id
    ).first()

    if not step:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pathway step not found or unauthorized access."
        )

    step.is_completed = not step.is_completed
    step.completed_at = datetime.utcnow() if step.is_completed else None

    # Recalculate pathway progress percentage
    pathway = step.pathway
    all_steps = db.query(PathwayStep).filter(PathwayStep.pathway_id == pathway.id).all()
    completed_count = sum(1 for s in all_steps if s.is_completed)
    pathway.progress_percentage = round((completed_count / max(len(all_steps), 1)) * 100.0, 1)

    # Also update student progress completed steps
    prog = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id,
        StudentProgress.skill_code == step.skill_code
    ).first()
    if prog:
        if step.is_completed:
            prog.completed_steps += 1
            prog.total_time_spent_mins += int(step.duration_hours * 60)
        else:
            prog.completed_steps = max(0, prog.completed_steps - 1)

    db.commit()
    db.refresh(pathway)

    steps_resp = [PathwayStepResponse.model_validate(st) for st in all_steps]
    resp = PathwayResponse.model_validate(pathway)
    resp.steps = steps_resp
    return resp
