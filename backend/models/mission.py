from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class DailyMission(Base):
    __tablename__ = "daily_missions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    mission_type = Column(String(50), default="practice") # quiz, practice, reading, challenge
    skill_code = Column(String(50), default="python")
    xp_reward = Column(Integer, default=50)
    target_url = Column(String(500), nullable=True)
    is_completed = Column(Boolean, default=False)
    streak_count = Column(Integer, default=1)
    assigned_date = Column(Date, default=date.today)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="missions")
