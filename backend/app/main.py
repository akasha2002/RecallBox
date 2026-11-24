from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy import text

from app.core.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)
from app.core.logging import RequestLoggingMiddleware
from app.api.v1.router import api_router
from app.schemas.health import HealthResponse
from app.db.session import SessionLocal

# Initialize FastAPI application with OpenAPI metadata
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend REST API for RecallBox - Personal Note Management Application",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Register Request Logging Middleware (logs method, path, status, and latency)
app.add_middleware(RequestLoggingMiddleware)

# Configure Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Centralized Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Include API v1 routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get(
    "/",
    summary="API Root",
    description="Welcome endpoint providing API status and documentation links.",
    tags=["Root"],
)
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Convenience Health Check",
    description="Top-level health check endpoint mirroring the health status.",
)
async def root_health():
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
