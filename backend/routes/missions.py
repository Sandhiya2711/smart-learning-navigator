from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.user import User
from backend.models.mission import DailyMission
from backend.models.assessment import AssessmentSubmission
from backend.schemas import MissionResponse
from backend.services.auth import get_current_user

router = APIRouter(prefix="/missions", tags=["Daily Missions"])

@router.get("/today", response_model=List[MissionResponse])
def get_today_missions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    today = date.today()
    missions = db.query(DailyMission).filter(
        DailyMission.user_id == current_user.id,
        DailyMission.assigned_date == today
    ).all()

    if not missions:
        # Check user's latest gaps to generate tailored missions
        latest_sub = db.query(AssessmentSubmission).filter(
            AssessmentSubmission.user_id == current_user.id
        ).order_by(AssessmentSubmission.submitted_at.desc()).first()

        gap_skill = "sql"
        if latest_sub and latest_sub.knowledge_gaps:
            gap_skill = latest_sub.knowledge_gaps[0].get("skill_code", "sql")

        # Generate fresh missions for today
        new_missions = [
            DailyMission(
                user_id=current_user.id,
                title=f"Address {gap_skill.upper()} Diagnostic Knowledge Gap",
                description=f"Review targeted lessons and resolve high-priority conceptual gaps in {gap_skill}.",
                mission_type="practice",
                skill_code=gap_skill,
                xp_reward=60,
                target_url=None,
                is_completed=False,
                streak_count=1,
                assigned_date=today
            ),
            DailyMission(
                user_id=current_user.id,
                title="Pathway Stage Checkpoint Quiz",
                description="Complete the comprehension quiz for your active pathway stage.",
                mission_type="quiz",
                skill_code="web_dev",
                xp_reward=80,
                target_url=None,
                is_completed=False,
                streak_count=1,
                assigned_date=today
            ),
            DailyMission(
                user_id=current_user.id,
                title="Python Clean Code & Testing Drill",
                description="Write unit test assertions for your recent problem-solving code.",
                mission_type="challenge",
                skill_code="python",
                xp_reward=100,
                target_url="https://docs.python.org/3/tutorial/",
                is_completed=False,
                streak_count=1,
                assigned_date=today
            )
        ]
        db.add_all(new_missions)
        db.commit()
        missions = new_missions

    return missions

@router.post("/{mission_id}/complete")
def complete_mission(
    mission_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mission = db.query(DailyMission).filter(
        DailyMission.id == mission_id,
        DailyMission.user_id == current_user.id
    ).first()

    if not mission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mission not found."
        )

    if not mission.is_completed:
        mission.is_completed = True
        mission.completed_at = datetime.utcnow()
        mission.streak_count += 1
        db.commit()

    return {
        "status": "completed",
        "mission_id": mission.id,
        "xp_earned": mission.xp_reward,
        "new_streak": mission.streak_count
    }
