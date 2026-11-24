from typing import Any, Generic, List, Optional, TypeVar, Union
from uuid import UUID
from sqlalchemy.orm import Session
from app.core.exceptions import NotFoundException
from app.repositories.base import BaseRepository
from app.schemas.common import PaginationParams, PaginatedResponse

ModelType = TypeVar("ModelType")
RepoType = TypeVar("RepoType", bound=BaseRepository)


class BaseService(Generic[ModelType, RepoType]):
    """
    Base service layer containing business logic and coordinating with repositories.
    """

    def __init__(self, repository: RepoType, resource_name: str = "Resource"):
        self.repository = repository
        self.resource_name = resource_name

    def get_or_404(self, db: Session, id: Union[UUID, str, int]) -> ModelType:
        """Fetch entity by ID or raise standardized NotFoundException (404)."""
        entity = self.repository.get(db, id)
        if not entity:
            raise NotFoundException(resource=self.resource_name, identifier=id)
        return entity

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Fetch multiple entities."""
        return self.repository.get_multi(db, skip=skip, limit=limit)

    def get_paginated(
        self, db: Session, *, params: PaginationParams
    ) -> PaginatedResponse[ModelType]:
        """Fetch paginated list with total count."""
        items = self.repository.get_multi(db, skip=params.offset, limit=params.limit)
        total = self.repository.count(db)
        return PaginatedResponse.create(items=items, total=total, params=params)

    def delete(self, db: Session, id: Union[UUID, str, int]) -> ModelType:
        """Delete entity by ID or raise NotFoundException."""
        entity = self.get_or_404(db, id)
        self.repository.remove(db, id=id)
        return entity
