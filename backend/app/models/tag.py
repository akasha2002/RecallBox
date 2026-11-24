import uuid
from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.models.note_tag import note_tags


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (
        UniqueConstraint("workspace_id", "name", name="uq_tag_workspace_name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    workspace_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    workspace = relationship("Workspace", back_populates="tags")
    notes = relationship("Note", secondary=note_tags, back_populates="tags")

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name={self.name}, workspace_id={self.workspace_id})>"
