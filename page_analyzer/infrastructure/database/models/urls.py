from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from page_analyzer.infrastructure.database.id_mixins.created_at_mixins import \
    CreatedAtMixin
from page_analyzer.infrastructure.database.id_mixins.id_mixins import IdMixin
from page_analyzer.infrastructure.database.models.base import Base


class Urls(Base, IdMixin, CreatedAtMixin):
    name: Mapped[str] = mapped_column(String, nullable=False)
