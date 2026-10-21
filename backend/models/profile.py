from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    education_level = Column(String(100), default="Bachelor's Degree") # e.g. High School, Bachelor's, Master's
    branch = Column(String(100), default="Computer Science")           # e.g. CS, IT, ECE, Data Science
    career_goal = Column(String(150), default="Full-Stack Web Developer") # e.g. AI/ML Engineer, Full-Stack, Data Scientist
    preferred_learning_style = Column(String(100), default="Hands-on Project") # Visual, Hands-on Project, Reading/Theory
    daily_study_hours = Column(Float, default=2.0)
    target_date = Column(String(50), nullable=True) # Target completion ISO date
    current_skills = Column(JSON, default=list) # List of skill codes e.g. ["python", "sql"]
    bio = Column(Text, nullable=True)
    avatar_config = Column(JSON, default=dict) # Theme, colors, accessories, reduced_motion
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")
