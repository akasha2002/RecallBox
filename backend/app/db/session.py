from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

engine = None
SessionLocal = None

if settings.DATABASE_URL:
    db_url = settings.DATABASE_URL
    # Ensure standard postgresql:// URLs use psycopg2 driver if no driver is specified
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    engine = create_engine(
        db_url,
        pool_pre_ping=True,  # Test connections before giving them to sessions
        pool_recycle=300,    # Recycle connections after 5 minutes
        pool_size=5,
        max_overflow=10,
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a database session for a request
    and ensuring proper closure upon completion.
    """
    if SessionLocal is None:
        raise RuntimeError("Database connection is not configured. Please set DATABASE_URL in .env.")
    
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
