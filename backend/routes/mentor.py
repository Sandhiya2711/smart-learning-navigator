from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from backend.database import get_db
from backend.models.user import User
from backend.models.profile import StudentProfile
from backend.models.assessment import AssessmentSubmission
from backend.schemas import MentorQueryRequest, MentorQueryResponse
from backend.services.auth import get_optional_current_user
from backend.services.mentor import generate_mentor_guidance

router = APIRouter(prefix="/mentor", tags=["Study Mentor"])

@router.post("/recommend", response_model=MentorQueryResponse)
def get_mentor_recommendation(
    req: MentorQueryRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    user_profile = None
    gaps = None

    if current_user:
        profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
        if profile:
            user_profile = {
                "career_goal": profile.career_goal,
                "daily_study_hours": profile.daily_study_hours,
                "learning_style": profile.preferred_learning_style
            }
        latest_sub = db.query(AssessmentSubmission).filter(
            AssessmentSubmission.user_id == current_user.id
        ).order_by(AssessmentSubmission.submitted_at.desc()).first()
        if latest_sub:
            gaps = latest_sub.knowledge_gaps

    result = generate_mentor_guidance(
        user_message=req.message,
        context_skill=req.context_skill,
        user_profile=user_profile,
        gaps=gaps
    )

    return MentorQueryResponse(
        reply=result["reply"],
        suggested_actions=result.get("suggested_actions", []),
        generated_at=result["generated_at"]
    )
