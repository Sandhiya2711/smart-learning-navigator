from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.database import Base

class StudentProgress(Base):
    __tablename__ = "student_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_code = Column(String(50), nullable=False)
    proficiency_score = Column(Float, default=0.0) # 0 to 100
    proficiency_level = Column(String(50), default="Novice") # Novice, Intermediate, Advanced, Master
    completed_steps = Column(Integer, default=0)
    total_time_spent_mins = Column(Integer, default=0)
    last_active_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="progress")

    __table_args__ = (
        UniqueConstraint("user_id", "skill_code", name="uq_user_skill_progress"),
    )
