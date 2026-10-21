from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    step_id = Column(Integer, ForeignKey("pathway_steps.id", ondelete="SET NULL"), nullable=True)
    skill_code = Column(String(50), nullable=False)
    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=5)
    percentage = Column(Float, default=0.0)
    passed = Column(Boolean, default=False)
    taken_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quiz_results")
