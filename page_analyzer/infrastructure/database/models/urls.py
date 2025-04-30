import datetime
import uuid

from sqlalchemy import UUID, Date, func, String
from sqlalchemy.orm import Mapped, mapped_column

from page_analyzer.infrastructure.database.models.base import Base


class Urls(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime.date] = mapped_column(
        Date,
        server_default=func.current_date(),
        default=datetime.date.today,
    )