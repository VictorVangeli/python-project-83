from sqlalchemy import ForeignKey, String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from page_analyzer.infrastructure.database.id_mixins.created_at_mixins import (
    CreatedAtMixin,
)
from page_analyzer.infrastructure.database.id_mixins.id_mixins import IdMixin
from page_analyzer.infrastructure.database.models.base import Base


class UrlChecks(Base, IdMixin, CreatedAtMixin):
    url_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("urls.id", ondelete="CASCADE"), nullable=False
    )
    status_code: Mapped[int] = mapped_column(Integer, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    h1: Mapped[str] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
