"""add savings goals and contributions

Revision ID: bc9f2bcacd60
Revises: b7f2c94a1d3e
Create Date: 2026-10-24 21:32:12.460970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'bc9f2bcacd60'
down_revision: Union[str, Sequence[str], None] = 'b7f2c94a1d3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'savings_goals',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('target_amount', sa.BigInteger(), nullable=False),
        sa.Column('target_date', sa.Date(), nullable=True),
        sa.Column('status', sa.Enum('ACTIVE', 'ON_HOLD', 'COMPLETED', name='savinggoalstatus', native_enum=False, length=16), server_default='ACTIVE', nullable=False),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('target_amount > 0', name='target_positive'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_savings_goals_user', 'savings_goals', ['user_id'], unique=False, postgresql_where=sa.text('deleted_at IS NULL'))

    op.create_table(
        'savings_contributions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('goal_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('amount', sa.BigInteger(), nullable=False),
        sa.Column('contributed_at', sa.Date(), nullable=False),
        sa.Column('note', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('amount <> 0', name='amount_nonzero'),
        sa.ForeignKeyConstraint(['goal_id'], ['savings_goals.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_contrib_goal_date', 'savings_contributions', ['goal_id', 'contributed_at'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_contrib_goal_date', table_name='savings_contributions')
    op.drop_table('savings_contributions')
    op.drop_index('ix_savings_goals_user', table_name='savings_goals', postgresql_where=sa.text('deleted_at IS NULL'))
    op.drop_table('savings_goals')
