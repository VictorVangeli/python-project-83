import datetime
import uuid

from sqlalchemy import UUID, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column

from page_analyzer.infrastructure.models.base import Base


class Urls(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.datetime.now,
    )