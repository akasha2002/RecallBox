from typing import TypeVar, Generic, List, Optional, Any
import math
from pydantic import BaseModel, Field

T = TypeVar("T")


class MessageResponse(BaseModel):
    """Standard message response for actions (e.g. deletion, acknowledgment)."""
    message: str
    success: bool = True


class ErrorDetail(BaseModel):
    """Field-specific validation error details."""
    field: str
    message: str
    type: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response structure returned across all API endpoints."""
    success: bool = False
    error_code: str
    message: str
    details: Optional[Any] = None


class PaginationParams(BaseModel):
    """Standard query parameters for paginated endpoints."""
    page: int = Field(default=1, ge=1, description="Page number starting from 1")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page (1-100)")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard generic wrapper for paginated list responses."""
    items: List[T]
    total: int = Field(description="Total count of items across all pages")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Number of items per page")
    total_pages: int = Field(description="Total number of pages")

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams) -> "PaginatedResponse[T]":
        total_pages = math.ceil(total / params.page_size) if total > 0 else 1
        return cls(
            items=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
        )


class DataResponse(BaseModel, Generic[T]):
    """Standard generic wrapper for single entity responses."""
    success: bool = True
    data: T
