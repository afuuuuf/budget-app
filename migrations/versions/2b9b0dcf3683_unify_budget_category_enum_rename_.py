"""unify budget category enum, rename budget_type column to category

Revision ID: 2b9b0dcf3683
Revises: 624344bd3983
Create Date: 2026-11-03 01:43:21.020174

Manually rewritten from autogen: autogen rendered add+drop (which would
discard existing budget rows' category). Changed to an in-place RENAME
that preserves data. The column is plain VARCHAR (native_enum=False), so
renaming is safe and existing values (BILLS, SHOPPING, ...) remain valid
in the merged Category enum.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b9b0dcf3683'
down_revision: Union[str, Sequence[str], None] = '624344bd3983'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'budgets',
        'budget_type',
        new_column_name='category',
        existing_type=sa.String(),
        existing_nullable=False,
    )
    op.alter_column(
        'budgets',
        'category',
        type_=sa.Enum(
            'FOOD', 'BILLS', 'SHOPPING', 'TRANSPORTATION',
            'ENTERTAINMENT', 'OTHERS', name='category',
            native_enum=False, length=20,
        ),
        existing_type=sa.String(),
        existing_nullable=False,
    )
    op.drop_index(op.f('ix_budgets_budget_type'), table_name='budgets')
    op.create_index(op.f('ix_budgets_category'), 'budgets', ['category'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_budgets_category'), table_name='budgets')
    op.create_index(op.f('ix_budgets_budget_type'), 'budgets', ['category'], unique=False)
    op.alter_column(
        'budgets',
        'category',
        type_=sa.String(),
        existing_type=sa.Enum(
            'FOOD', 'BILLS', 'SHOPPING', 'TRANSPORTATION',
            'ENTERTAINMENT', 'OTHERS', name='category',
            native_enum=False, length=20,
        ),
        existing_nullable=False,
    )
    op.alter_column(
        'budgets',
        'category',
        new_column_name='budget_type',
        existing_type=sa.String(),
        existing_nullable=False,
    )
