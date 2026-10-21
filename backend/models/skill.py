from sqlalchemy import Column, Integer, String, Text, JSON
from backend.database import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False) # e.g. "python", "java", "sql", "data_analytics", "web_dev", "ml"
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon_name = Column(String(50), default="Code")
    difficulty = Column(String(50), default="Intermediate")
    prerequisites = Column(JSON, default=list) # List of prerequisite skill codes
    color_hex = Column(String(20), default="#8b5cf6")
    galaxy_orbit_radius = Column(Integer, default=140)
