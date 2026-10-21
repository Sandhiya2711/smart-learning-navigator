from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database import Base

class LearningPathway(Base):
    __tablename__ = "learning_pathways"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_goal = Column(String(150), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_date = Column(String(50), nullable=True)
    total_duration_weeks = Column(Integer, default=12)
    progress_percentage = Column(Float, default=0.0)
    status = Column(String(50), default="active") # active, completed, archived
    generated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="pathways")
    steps = relationship("PathwayStep", back_populates="pathway", order_by="PathwayStep.order_index", cascade="all, delete-orphan")

class PathwayStep(Base):
    __tablename__ = "pathway_steps"

    id = Column(Integer, primary_key=True, index=True)
    pathway_id = Column(Integer, ForeignKey("learning_pathways.id", ondelete="CASCADE"), nullable=False)
    order_index = Column(Integer, nullable=False) # 1, 2, 3...
    skill_code = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    stage_name = Column(String(100), default="Foundation") # e.g. Stage 1: Core Fundamentals, Stage 2: Deep Dive
    description = Column(Text, nullable=True)
    duration_hours = Column(Float, default=10.0)
    learning_objectives = Column(JSON, default=list) # List of bullet points
    resources = Column(JSON, default=list)           # List of recommended resource dicts
    quiz_data = Column(JSON, default=list)           # Mini checkpoint quiz questions
    practical_tasks = Column(JSON, default=list)     # Hands-on challenges/projects
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    pathway = relationship("LearningPathway", back_populates="steps")
