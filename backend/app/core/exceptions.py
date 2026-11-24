from typing import Any, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger("recallbox.exceptions")


class AppException(Exception):
    """Base application exception with status code and error code."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: str = "INTERNAL_ERROR",
        details: Optional[Any] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details


class NotFoundException(AppException):
    """Resource not found (HTTP 404)."""

    def __init__(self, resource: str, identifier: Any = None):
        msg = f"{resource} not found" if identifier is None else f"{resource} with identifier '{identifier}' not found"
        super().__init__(
            message=msg,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
        )


class UnauthorizedException(AppException):
    """Authentication failed or missing credentials (HTTP 401)."""

    def __init__(self, message: str = "Invalid or expired credentials"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
        )


class ForbiddenException(AppException):
    """Access denied / Workspace isolation violation (HTTP 403)."""

    def __init__(self, message: str = "You do not have permission to access this resource"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
        )


class ConflictException(AppException):
    """Resource conflict, e.g. duplicate name in workspace (HTTP 409)."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
        )


class BadRequestException(AppException):
    """Invalid input or business logic violation (HTTP 400)."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="BAD_REQUEST",
            details=details,
        )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handles custom application exceptions."""
    logger.warning(
        "Application exception: %s [%s] on %s %s",
        exc.message,
        exc.error_code,
        request.method,
        request.url.path,
    )
    content = {
        "success": False,
        "error_code": exc.error_code,
        "message": exc.message,
    }
    if exc.details is not None:
        content["details"] = exc.details

    return JSONResponse(
        status_code=exc.status_code,
        content=content,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Formats Pydantic request validation errors into clean, readable JSON."""
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err.get("loc", []) if loc != "body")
        errors.append({
            "field": field or "body",
            "message": err.get("msg", "Invalid value"),
            "type": err.get("type", "value_error"),
        })

    logger.warning("Validation error on %s %s: %s", request.method, request.url.path, errors)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error_code": "VALIDATION_ERROR",
            "message": "Input validation failed. Please check the supplied fields.",
            "details": errors,
        },
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catches unhandled errors without leaking sensitive stack traces or credentials."""
    logger.exception("Unhandled exception on %s %s: %s", request.method, request.url.path, str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )
