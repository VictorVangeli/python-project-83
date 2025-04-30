import datetime

from sqlalchemy import func, Date
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    created_at: Mapped[datetime.date] = mapped_column(
        Date,
        server_default=func.current_date(),
        default=datetime.date.today,
    )
