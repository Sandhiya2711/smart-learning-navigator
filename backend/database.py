import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+psycopg2://postgres:postgrespassword@localhost:5432/skillverse"
)

# Connect to database with resilient fallback
try:
    if DATABASE_URL.startswith("postgresql"):
        # Test connecting to Postgres
        engine = create_engine(
            DATABASE_URL, 
            pool_pre_ping=True, 
            connect_args={"connect_timeout": 3}
        )
        with engine.connect() as conn:
            logger.info("Successfully connected to PostgreSQL database.")
    else:
        engine = create_engine(
            DATABASE_URL, 
            connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
        )
except Exception as e:
    logger.warning(
        f"PostgreSQL connection to {DATABASE_URL} could not be established ({e}). "
        "Falling back to local SQLite database 'sqlite:///./skillverse.db'. "
        "To use PostgreSQL, start container with 'docker compose up -d'."
    )
    DATABASE_URL = "sqlite:///./skillverse.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
