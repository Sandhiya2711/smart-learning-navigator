import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from backend.config import settings
from backend.database import engine, Base, SessionLocal, get_db
from backend.services.seed import seed_database
from backend.routes import (
    auth,
    students,
    skills,
    assessment,
    pathways,
    resources,
    missions,
    analytics,
    mentor,
    avatar,
    viva_certificates,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("skillverse")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables created and seed data initialized
    logger.info("Initializing SkillVerse AI Database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
    finally:
        db.close()
    yield
    logger.info("SkillVerse AI Server shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="SkillVerse AI — Smart Learning Pathway Navigator REST API",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check Endpoint
@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(Base.metadata.tables["users"].select().limit(1))
    except Exception as e:
        db_status = f"degraded ({e})"

    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": db_status
    }

# Mount Routers under both /api and root level for maximum client compatibility
routers = [
    auth.router,
    students.router,
    skills.router,
    assessment.router,
    pathways.router,
    resources.router,
    missions.router,
    analytics.router,
    mentor.router,
    avatar.router,
    viva_certificates.router
]

for r in routers:
    app.include_router(r, prefix="/api")
    app.include_router(r)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
