"""update urls check model

Revision ID: 0c4cf9d9a034
Revises: f062b81ca566
Create Date: 2025-04-30 15:12:04.000331

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0c4cf9d9a034"
down_revision: str | None = "f062b81ca566"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("url_checks", sa.Column("title", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("url_checks", "title")
    # ### end Alembic commands ###
