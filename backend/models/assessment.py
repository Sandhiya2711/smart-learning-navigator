from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database import Base

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), default="Comprehensive Diagnostic")
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan")

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    skill_code = Column(String(50), index=True, nullable=False) # e.g. python, java, sql, data_analytics, web_dev, ml
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False) # list of strings
    correct_option_index = Column(Integer, nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(String(50), default="Intermediate")
    topic = Column(String(100), nullable=True)

    assessment = relationship("Assessment", back_populates="questions")

class AssessmentSubmission(Base):
    __tablename__ = "assessment_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_score = Column(Float, default=0.0)
    skill_scores = Column(JSON, default=dict) # e.g. {"python": 80, "sql": 40, ...}
    knowledge_gaps = Column(JSON, default=list) # e.g. [{"skill": "sql", "topic": "JOIN Operations", "severity": "High"}]
    submitted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="submissions")
    answers = relationship("AssessmentAnswer", back_populates="submission", cascade="all, delete-orphan")

class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("assessment_submissions.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("assessment_questions.id", ondelete="CASCADE"), nullable=False)
    selected_option = Column(Integer, nullable=False)
    is_correct = Column(Integer, default=0) # 1 if correct, 0 if false

    submission = relationship("AssessmentSubmission", back_populates="answers")
