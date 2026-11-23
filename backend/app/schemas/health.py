from datetime import datetime, timezone
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="ok", description="Current health status of the API")
    app: str = Field(default="RecallBox API", description="Name of the application")
    version: str = Field(default="1.0.0", description="Application version")
    environment: str = Field(default="development", description="Current running environment")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Current UTC timestamp"
    )
