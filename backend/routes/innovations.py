from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from pydantic import BaseModel
from backend.database import get_db
from backend.models.user import User
from backend.models.profile import StudentProfile
from backend.models.assessment import AssessmentSubmission
from backend.models.pathway import LearningPathway, PathwayStep
from backend.models.resource import LearningResource
from backend.services.auth import get_optional_current_user, get_current_user
from backend.services.innovations import (
    simulate_parallel_universes,
    analyze_mistake_dna,
    get_skill_ripple,
    get_all_ripples
)
from backend.services.recommender import recommender_engine

router = APIRouter(prefix="/innovations", tags=["Innovations"])

class ActivateUniverseRequest(BaseModel):
    universe_id: str
    career_goal: str
    sequence: List[str]

@router.get("/parallel-universes")
def get_parallel_universes(
    current_user: User = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    career_goal = "Full-Stack Web Developer"
    student_scores = {"python": 50, "sql": 40, "web_dev": 40, "data_analytics": 30, "java": 20, "ml": 20}

    if current_user:
        profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
        if profile and profile.career_goal:
            career_goal = profile.career_goal

        latest_sub = db.query(AssessmentSubmission).filter(
            AssessmentSubmission.user_id == current_user.id
        ).order_by(AssessmentSubmission.submitted_at.desc()).first()
        if latest_sub and latest_sub.skill_scores:
            student_scores = latest_sub.skill_scores

    universes = simulate_parallel_universes(career_goal, student_scores)
    return {
        "career_goal": career_goal,
        "student_baseline_scores": student_scores,
        "universes": universes
    }

@router.post("/parallel-universes/activate")
def activate_parallel_universe(
    req: ActivateUniverseRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    daily_hours = profile.daily_study_hours if profile else 2.0
    target_date = profile.target_date if profile else None

    # Fetch resources catalog
    all_res = db.query(LearningResource).all()
    res_dicts = [
        {"id": r.id, "title": r.title, "skill_code": r.skill_code, "category": r.category, "url": r.url, "is_free": r.is_free, "difficulty": r.difficulty, "provider": r.provider, "description": r.description}
        for r in all_res
    ]

    latest_sub = db.query(AssessmentSubmission).filter(
        AssessmentSubmission.user_id == current_user.id
    ).order_by(AssessmentSubmission.submitted_at.desc()).first()
    skill_scores = latest_sub.skill_scores if latest_sub else {"python": 50, "sql": 40, "web_dev": 40}
    gaps = latest_sub.knowledge_gaps if latest_sub else []

    # Generate custom ordered pathway according to the chosen parallel sequence
    generated = recommender_engine.generate_pathway(
        career_goal=req.career_goal,
        skill_scores=skill_scores,
        gaps=gaps,
        daily_study_hours=daily_hours,
        resources_catalog=res_dicts
    )

    # Reorder or filter steps to match the selected universe sequence
    ordered_steps = []
    step_map = {st["skill_code"]: st for st in generated["steps"]}
    order_idx = 1
    for code in req.sequence:
        if code in step_map:
            st = step_map[code].copy()
            st["order_index"] = order_idx
            ordered_steps.append(st)
            order_idx += 1

    # Archive previous pathways
    existing = db.query(LearningPathway).filter(
        LearningPathway.user_id == current_user.id,
        LearningPathway.status == "active"
    ).all()
    for ep in existing:
        ep.status = "archived"

    new_pathway = LearningPathway(
        user_id=current_user.id,
        career_goal=req.career_goal,
        title=f"Parallel Timeline: {req.career_goal}",
        description=f"Active Timeline [{req.universe_id}]. Customized route prioritizing: {' → '.join([s.title() for s in req.sequence])}",
        target_date=target_date,
        total_duration_weeks=generated["total_duration_weeks"],
        progress_percentage=0.0,
        status="active"
    )
    db.add(new_pathway)
    db.commit()
    db.refresh(new_pathway)

    for st_data in ordered_steps:
        step = PathwayStep(
            pathway_id=new_pathway.id,
            order_index=st_data["order_index"],
            skill_code=st_data["skill_code"],
            stage_name=st_data["stage_name"],
            title=st_data["title"],
            description=st_data["description"],
            duration_hours=st_data["duration_hours"],
            learning_objectives=st_data["learning_objectives"],
            resources=st_data["resources"],
            quiz_data=st_data["quiz_data"],
            practical_tasks=st_data["practical_tasks"],
            is_completed=False
        )
        db.add(step)

    db.commit()
    return {
        "status": "activated",
        "universe_id": req.universe_id,
        "pathway_id": new_pathway.id,
        "message": f"Successfully shifted universe to {req.universe_id}!"
    }

@router.get("/mistake-dna")
def get_mistake_dna(
    current_user: User = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    gaps = []
    if current_user:
        latest_sub = db.query(AssessmentSubmission).filter(
            AssessmentSubmission.user_id == current_user.id
        ).order_by(AssessmentSubmission.submitted_at.desc()).first()
        if latest_sub and latest_sub.knowledge_gaps:
            gaps = latest_sub.knowledge_gaps

    dna_results = analyze_mistake_dna(gaps)
    return {
        "total_dna_patterns": len(dna_results),
        "patterns": dna_results
    }

@router.get("/skill-ripple/{skill_code}")
def get_ripple_for_skill(skill_code: str):
    return get_skill_ripple(skill_code.lower())

@router.get("/skill-ripple")
def get_all_skill_ripples():
    return get_all_ripples()
