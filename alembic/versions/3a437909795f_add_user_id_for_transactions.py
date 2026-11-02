"""add user id for transactions

Revision ID: 3a437909795f
Revises: f6c39278df08
Create Date: 2026-10-30 23:19:28.166221

Manually written: autogen rendered user_id as nullable=False (would fail on
existing rows) and an unnamed FK (would fail on downgrade). Same null-safe
pattern as d85f3c9a4f94 (budgets).

Existing transactions rows had no user; they are backfilled to the primary
user (wnafif02@gmail.com) before tightening to NOT NULL. The category and
transaction_flow enums are modeled with native_enum=False, which PostgreSQL
stores as plain VARCHAR — no column alteration is needed for them.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3a437909795f'
down_revision: Union[str, Sequence[str], None] = 'f6c39278df08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PRIMARY_USER_EMAIL = "wnafif02@gmail.com"


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('transactions', sa.Column('user_id', sa.String(), nullable=True))

    bind = op.get_bind()
    transactions = sa.table(
        'transactions',
        sa.column('id', sa.String),
        sa.column('user_id', sa.String),
    )
    users = sa.table(
        'users',
        sa.column('id', sa.String),
        sa.column('email', sa.String),
    )
    primary_id = bind.execute(
        sa.select(users.c.id).where(users.c.email == PRIMARY_USER_EMAIL)
    ).scalar()
    if primary_id is None:
        raise RuntimeError(
            f"Primary user '{PRIMARY_USER_EMAIL}' not found; aborting to avoid "
            "a NOT NULL column with null rows."
        )

    bind.execute(
        transactions.update()
        .where(transactions.c.user_id.is_(None))
        .values(user_id=primary_id)
    )
    op.alter_column('transactions', 'user_id', existing_type=sa.String(), nullable=False)
    op.create_foreign_key(
        op.f('fk_transactions_user_id_users'),
        'transactions',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE',
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('fk_transactions_user_id_users'), 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'user_id')
