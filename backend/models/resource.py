from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime
from backend.database import Base

class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    skill_code = Column(String(50), index=True, nullable=False)
    category = Column(String(100), default="General") # e.g. Frontend, Backend, Machine Learning, Database
    resource_type = Column(String(50), default="documentation") # documentation, tutorial, video, practice, course
    url = Column(String(500), nullable=False)
    is_free = Column(Boolean, default=True)
    difficulty = Column(String(50), default="Beginner") # Beginner, Intermediate, Advanced
    rating = Column(Float, default=4.8)
    estimated_time = Column(String(50), default="2 hours")
    provider = Column(String(100), default="Official Docs")
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
