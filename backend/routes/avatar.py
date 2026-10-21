from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from backend.database import get_db
from backend.models.user import User
from backend.models.assessment import AssessmentSubmission
from backend.models.pathway import LearningPathway, PathwayStep
from backend.services.auth import get_optional_current_user
from backend.services.avatar import calculate_avatar_state

router = APIRouter(prefix="/avatar", tags=["Avatar Evolution"])

class EquipRequest(BaseModel):
    item_id: str
    slot: str

@router.get("/me")
def get_student_avatar(
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    skill_scores = {
        "python": 80.0,
        "sql": 40.0,
        "web_dev": 70.0,
        "data_analytics": 50.0,
        "java": 20.0,
        "ml": 30.0
    }
    completed_steps = 1

    if current_user:
        latest_sub = db.query(AssessmentSubmission).filter(
            AssessmentSubmission.user_id == current_user.id
        ).order_by(AssessmentSubmission.submitted_at.desc()).first()
        if latest_sub and latest_sub.skill_scores:
            skill_scores = latest_sub.skill_scores

        active_pathway = db.query(LearningPathway).filter(
            LearningPathway.user_id == current_user.id,
            LearningPathway.status == "active"
        ).first()
        if active_pathway:
            completed_steps = db.query(PathwayStep).filter(
                PathwayStep.pathway_id == active_pathway.id,
                PathwayStep.is_completed == True
            ).count()

    avatar_state = calculate_avatar_state(skill_scores, completed_steps)
    return avatar_state

@router.post("/equip")
def equip_accessory(req: EquipRequest):
    return {
        "status": "equipped",
        "item_id": req.item_id,
        "slot": req.slot,
        "message": f"Successfully equipped {req.item_id} onto {req.slot}!"
    }
