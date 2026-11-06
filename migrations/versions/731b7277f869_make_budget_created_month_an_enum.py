"""make budget created_month an enum

Revision ID: 731b7277f869
Revises: 2b9b0dcf3683
Create Date: 2026-11-06 09:46:02.168666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '731b7277f869'
down_revision: Union[str, Sequence[str], None] = '2b9b0dcf3683'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


MONTHS = (
    "ARRAY['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE',"
    "'JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER']"
)


def upgrade() -> None:
    """Upgrade schema."""
    # budgets: normalize casing ("November" -> "NOVEMBER"), then backfill nulls,
    # BEFORE tightening to NOT NULL
    op.execute(
        "UPDATE budgets SET created_month = UPPER(TRIM(created_month)) "
        "WHERE created_month IS NOT NULL"
    )
    op.execute(
        f"UPDATE budgets SET created_month = ({MONTHS})[EXTRACT(MONTH FROM created_at)::int] "
        "WHERE created_month IS NULL"
    )
    op.alter_column(
        "budgets", "created_month",
        existing_type=sa.VARCHAR(), type_=sa.String(length=20),
        existing_nullable=True, nullable=False,
    )

    # transactions: add as nullable, backfill from created_at, then tighten
    op.add_column(
        "transactions",
        sa.Column("created_month", sa.String(length=20), nullable=True),
    )
    op.execute(
        f"UPDATE transactions SET created_month = ({MONTHS})[EXTRACT(MONTH FROM created_at)::int]"
    )
    op.alter_column(
        "transactions", "created_month",
        existing_type=sa.String(length=20), nullable=False,
    )

    # indexes (must match the models' __table_args__ exactly)
    op.create_index(
        "ix_transactions_user_month_created", "transactions",
        ["user_id", "created_month", "created_at"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ix_budgets_user_month", "budgets",
        ["user_id", "created_month"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_budgets_user_month", table_name="budgets")
    op.drop_index("ix_transactions_user_month_created", table_name="transactions")
    op.drop_column("transactions", "created_month")
    op.alter_column(
        "budgets", "created_month",
        existing_type=sa.String(length=20), type_=sa.String(),
        existing_nullable=False, nullable=True,
    )