from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    full_name: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Profile Schemas ---
class ProfileUpdateRequest(BaseModel):
    education_level: Optional[str] = "Bachelor's Degree"
    branch: Optional[str] = "Computer Science"
    career_goal: Optional[str] = "Full-Stack Web Developer"
    preferred_learning_style: Optional[str] = "Hands-on Project"
    daily_study_hours: Optional[float] = 2.0
    current_skills: Optional[List[str]] = []
    bio: Optional[str] = None
    avatar_config: Optional[Dict[str, Any]] = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    education_level: str
    branch: str
    career_goal: str
    preferred_learning_style: str
    daily_study_hours: float
    target_date: Optional[str]
    current_skills: List[str]
    bio: Optional[str]
    avatar_config: Optional[Dict[str, Any]] = {}

    class Config:
        from_attributes = True

# --- Skill Schemas ---
class SkillResponse(BaseModel):
    id: int
    code: str
    name: str
    category: str
    description: Optional[str]
    icon_name: str
    difficulty: str
    prerequisites: List[str]
    color_hex: str
    galaxy_orbit_radius: int
    # Enriched dynamic fields
    user_score: Optional[float] = 0.0
    proficiency_level: Optional[str] = "Novice"
    is_gap: Optional[bool] = False

    class Config:
        from_attributes = True

# --- Assessment Schemas ---
class QuestionOptionResponse(BaseModel):
    id: int
    question_text: str
    skill_code: str
    options: List[str]
    difficulty: str
    topic: Optional[str]

class SingleAnswer(BaseModel):
    question_id: int
    selected_option: int

class AssessmentSubmitRequest(BaseModel):
    answers: List[SingleAnswer]

class KnowledgeGapItem(BaseModel):
    skill_code: str
    topic: str
    severity: str # High, Medium, Low
    recommendation: str

class AssessmentSubmissionResponse(BaseModel):
    id: int
    user_id: int
    total_score: float
    skill_scores: Dict[str, float]
    knowledge_gaps: List[KnowledgeGapItem]
    submitted_at: datetime

# --- Pathway Schemas ---
class PathwayGenerateRequest(BaseModel):
    career_goal: Optional[str] = None
    daily_study_hours: Optional[float] = None
    target_date: Optional[str] = None

class PathwayStepResponse(BaseModel):
    id: int
    order_index: int
    skill_code: str
    stage_name: str
    title: str
    description: Optional[str]
    duration_hours: float
    learning_objectives: List[str]
    resources: List[Dict[str, Any]]
    quiz_data: List[Dict[str, Any]]
    practical_tasks: List[str]
    is_completed: bool
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

class PathwayResponse(BaseModel):
    id: int
    user_id: int
    career_goal: str
    title: str
    description: Optional[str]
    target_date: Optional[str]
    total_duration_weeks: int
    progress_percentage: float
    status: str
    generated_at: datetime
    steps: List[PathwayStepResponse] = []

    class Config:
        from_attributes = True

# --- Resource Schemas ---
class ResourceResponse(BaseModel):
    id: int
    title: str
    skill_code: str
    category: str
    resource_type: str
    url: str
    is_free: bool
    difficulty: str
    rating: float
    estimated_time: str
    provider: str
    description: Optional[str]
    is_bookmarked: Optional[bool] = False

    class Config:
        from_attributes = True

class BookmarkCreateRequest(BaseModel):
    resource_id: int
    notes: Optional[str] = None

# --- Mission Schemas ---
class MissionResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    mission_type: str
    skill_code: str
    xp_reward: int
    target_url: Optional[str]
    is_completed: bool
    streak_count: int
    assigned_date: date

    class Config:
        from_attributes = True

# --- Analytics Schemas ---
class SkillScoreData(BaseModel):
    skill_name: str
    skill_code: str
    student_score: float
    target_benchmark: float

class WeeklyStudyData(BaseModel):
    day: str
    hours: float

class AnalyticsResponse(BaseModel):
    skill_scores: List[SkillScoreData]
    weekly_hours: List[WeeklyStudyData]
    total_study_hours: float
    completed_steps_count: int
    total_steps_count: int
    current_streak: int
    knowledge_gaps: List[KnowledgeGapItem]
    next_recommended_step: Optional[PathwayStepResponse] = None

# --- Mentor Schemas ---
class MentorQueryRequest(BaseModel):
    message: str
    context_skill: Optional[str] = None

class MentorActionSuggestion(BaseModel):
    label: str
    action_type: str # navigate, quiz, resource
    target: str

class MentorQueryResponse(BaseModel):
    reply: str
    suggested_actions: List[MentorActionSuggestion] = []
    generated_at: datetime
