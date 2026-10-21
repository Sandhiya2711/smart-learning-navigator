from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.skill import Skill
from backend.models.progress import StudentProgress
from backend.models.assessment import AssessmentSubmission
from backend.models.user import User
from backend.schemas import SkillResponse
from backend.services.auth import get_optional_current_user

router = APIRouter(prefix="/skills", tags=["Skills"])

@router.get("", response_model=List[SkillResponse])
def get_skills_catalog(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_optional_current_user)
):
    skills = db.query(Skill).all()
    user_progress_map = {}
    gap_skills = set()

    if current_user:
        progs = db.query(StudentProgress).filter(StudentProgress.user_id == current_user.id).all()
        user_progress_map = {p.skill_code: (p.proficiency_score, p.proficiency_level) for p in progs}
        
        last_sub = db.query(AssessmentSubmission).filter(
            AssessmentSubmission.user_id == current_user.id
        ).order_by(AssessmentSubmission.submitted_at.desc()).first()
        
        if last_sub and last_sub.knowledge_gaps:
            gap_skills = {g.get("skill_code") for g in last_sub.knowledge_gaps}

    result = []
    for s in skills:
        score, level = user_progress_map.get(s.code, (0.0, "Novice"))
        is_gap = s.code in gap_skills
        result.append(
            SkillResponse(
                id=s.id,
                code=s.code,
                name=s.name,
                category=s.category,
                description=s.description,
                icon_name=s.icon_name,
                difficulty=s.difficulty,
                prerequisites=s.prerequisites or [],
                color_hex=s.color_hex or "#8b5cf6",
                galaxy_orbit_radius=s.galaxy_orbit_radius or 150,
                user_score=score,
                proficiency_level=level,
                is_gap=is_gap
            )
        )
    return result
