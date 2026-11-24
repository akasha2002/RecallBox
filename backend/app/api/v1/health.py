from fastapi import APIRouter
from sqlalchemy import text
from app.schemas.health import HealthResponse
from app.core.config import settings
from app.db.session import SessionLocal

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the API service and database are healthy and operational."
)
async def get_health():
    db_status = "not_configured"
    if settings.DATABASE_URL and SessionLocal is not None:
        try:
            with SessionLocal() as session:
                session.execute(text("SELECT 1"))
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {type(e).__name__}"

    return HealthResponse(
        status="ok",
        app=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        database=db_status,
    )
