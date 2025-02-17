import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import TIMESTAMP, VARCHAR, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Base, TableNameMixin

if TYPE_CHECKING:
    from .audio import AudioRecord


class User(TableNameMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        VARCHAR(128), unique=True, index=True, nullable=False
    )
    access_token: Mapped[str] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )

    audio_records: Mapped[List["AudioRecord"]] = relationship(
        "AudioRecord", back_populates="user", lazy="selectin"
    )

    def __repr__(self):
        return f"{self.username} | {self.access_token}"
