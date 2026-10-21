from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.models.profile import StudentProfile
from backend.schemas import ProfileResponse, ProfileUpdateRequest
from backend.services.auth import get_current_user

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/me", response_model=ProfileResponse)
def get_current_student_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        profile = StudentProfile(
            user_id=current_user.id,
            education_level="Bachelor's Degree",
            branch="Computer Science",
            career_goal="Full-Stack Web Developer",
            preferred_learning_style="Hands-on Project",
            daily_study_hours=2.0
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("/me", response_model=ProfileResponse)
def update_current_student_profile(
    update_data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.add(profile)

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile
