"""restore users email unique and nullable columns

Revision ID: 7a9c505a3c21
Revises: ad9d17c6485a
Create Date: 2026-10-26 23:39:29.091993

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "7a9c505a3c21"
down_revision: Union[str, Sequence[str], None] = "ad9d17c6485a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(op.f("users_email_key"), "users", ["email"])
    op.alter_column(
        "users", "updated_at", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.alter_column(
        "transactions",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        nullable=True,
    )
    op.alter_column(
        "budgets", "updated_at", existing_type=postgresql.TIMESTAMP(), nullable=True
    )
    op.alter_column(
        "budgets", "created_month", existing_type=sa.VARCHAR(), nullable=True
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "budgets", "created_month", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "budgets", "updated_at", existing_type=postgresql.TIMESTAMP(), nullable=False
    )
    op.alter_column(
        "transactions",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        nullable=False,
    )
    op.alter_column(
        "users", "updated_at", existing_type=postgresql.TIMESTAMP(), nullable=False
    )
    op.drop_constraint(op.f("users_email_key"), "users", type_="unique")
