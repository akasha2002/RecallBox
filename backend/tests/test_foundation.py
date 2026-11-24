import uuid
import pytest
from fastapi import FastAPI, Depends, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

from app.core.exceptions import (
    AppException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    ConflictException,
    BadRequestException,
    app_exception_handler,
    validation_exception_handler,
)
from app.schemas.common import PaginationParams, PaginatedResponse, MessageResponse
from app.repositories.base import BaseRepository
from app.models.workspace import Workspace
from app.services.base import BaseService


# Helper test app for verifying exception handling and middleware
test_app = FastAPI()
test_app.add_exception_handler(AppException, app_exception_handler)
test_app.add_exception_handler(Exception, app_exception_handler)

from fastapi.exceptions import RequestValidationError
test_app.add_exception_handler(RequestValidationError, validation_exception_handler)


class SampleItem(BaseModel):
    name: str = Field(min_length=3)
    count: int = Field(gt=0)


@test_app.get("/test/not-found")
def trigger_not_found():
    raise NotFoundException(resource="Workspace", identifier="123")


@test_app.get("/test/unauthorized")
def trigger_unauthorized():
    raise UnauthorizedException("Invalid workspace access token")


@test_app.get("/test/forbidden")
def trigger_forbidden():
    raise ForbiddenException()


@test_app.get("/test/conflict")
def trigger_conflict():
    raise ConflictException("Category with this name already exists in workspace")


@test_app.get("/test/bad-request")
def trigger_bad_request():
    raise BadRequestException("Invalid date range supplied")


@test_app.post("/test/validation")
def trigger_validation(item: SampleItem):
    return item


test_client = TestClient(test_app)


def test_not_found_exception_handling():
    """Verify that NotFoundException produces uniform 404 JSON response."""
    response = test_client.get("/test/not-found")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["error_code"] == "NOT_FOUND"
    assert "Workspace" in data["message"]


def test_unauthorized_exception_handling():
    """Verify that UnauthorizedException produces uniform 401 JSON response."""
    response = test_client.get("/test/unauthorized")
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False
    assert data["error_code"] == "UNAUTHORIZED"
    assert "Invalid workspace access token" in data["message"]


def test_forbidden_exception_handling():
    """Verify that ForbiddenException produces uniform 403 JSON response."""
    response = test_client.get("/test/forbidden")
    assert response.status_code == 403
    data = response.json()
    assert data["success"] is False
    assert data["error_code"] == "FORBIDDEN"


def test_conflict_exception_handling():
    """Verify that ConflictException produces uniform 409 JSON response."""
    response = test_client.get("/test/conflict")
    assert response.status_code == 409
    data = response.json()
    assert data["success"] is False
    assert data["error_code"] == "CONFLICT"


def test_bad_request_exception_handling():
    """Verify that BadRequestException produces uniform 400 JSON response."""
    response = test_client.get("/test/bad-request")
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error_code"] == "BAD_REQUEST"


def test_validation_exception_handling():
    """Verify that Pydantic validation errors return structured 422 JSON with field errors."""
    response = test_client.post("/test/validation", json={"name": "a", "count": -5})
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert data["error_code"] == "VALIDATION_ERROR"
    assert isinstance(data["details"], list)
    fields = [d["field"] for d in data["details"]]
    assert "name" in fields
    assert "count" in fields


def test_pagination_params_calculation():
    """Verify that PaginationParams calculates offset and limit properly."""
    params = PaginationParams(page=3, page_size=15)
    assert params.offset == 30
    assert params.limit == 15


def test_paginated_response_helper():
    """Verify that PaginatedResponse correctly computes total_pages."""
    params = PaginationParams(page=1, page_size=10)
    items = ["item1", "item2", "item3"]
    paginated = PaginatedResponse.create(items=items, total=25, params=params)
    assert paginated.page == 1
    assert paginated.page_size == 10
    assert paginated.total == 25
    assert paginated.total_pages == 3
    assert len(paginated.items) == 3


def test_base_repository_and_service_interface():
    """Verify BaseRepository and BaseService instantiation and interface structure."""
    repo = BaseRepository(Workspace)
    service = BaseService(repository=repo, resource_name="Workspace")
    assert service.resource_name == "Workspace"
    assert service.repository.model == Workspace


def test_request_logging_header(client):
    """Verify that requests pass through logging middleware and receive X-Process-Time."""
    response = client.get("/")
    assert response.status_code == 200
    assert "X-Process-Time" in response.headers
