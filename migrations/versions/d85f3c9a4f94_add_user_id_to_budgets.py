"""add user_id to budgets

Revision ID: d85f3c9a4f94
Revises: 7a9c505a3c21
Create Date: 2026-10-30 22:11:08.792485

Manually cleaned 2026-10-30: autogen swept in unrelated drift (dropping
users_email_key, and toggling created_month/updated_at NOT NULL) that has
nothing to do with adding user_id. This revision only touches budgets.user_id.

Existing budgets rows had no user; they are backfilled to the primary user
(wnafif02@gmail.com) before tightening the column to NOT NULL. If the primary
user does not exist, the column is left nullable and the FK is skipped.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd85f3c9a4f94'
down_revision: Union[str, Sequence[str], None] = '7a9c505a3c21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PRIMARY_USER_EMAIL = "wnafif02@gmail.com"


def upgrade() -> None:
    """Upgrade schema."""
    # Add nullable first so existing rows are not rejected.
    op.add_column('budgets', sa.Column('user_id', sa.String(), nullable=True))

    # Backfill orphaned rows (those with no user_id) to the primary user.
    bind = op.get_bind()
    # Per-row update avoids relying on a correlated subquery
    # that target- and source-table are the same table.
    budgets = sa.table(
        'budgets',
        sa.column('id', sa.String),
        sa.column('user_id', sa.String),
    )
    users = sa.table(
        'users',
        sa.column('id', sa.String),
        sa.column('email', sa.String),
    )
    primary_id = bind.execute(sa.select(users.c.id).where(users.c.email == PRIMARY_USER_EMAIL)).scalar()
    if primary_id is not None:
        bind.execute(
            budgets.update()
            .where(budgets.c.user_id.is_(None))
            .values(user_id=primary_id)
        )
        # Now all rows have a user; tighten to NOT NULL and add the FK.
        op.alter_column(
            'budgets',
            'user_id',
            existing_type=sa.String(),
            nullable=False,
        )
        op.create_foreign_key(
            op.f('fk_budgets_user_id_users'),
            'budgets',
            'users',
            ['user_id'],
            ['id'],
            ondelete='CASCADE',
        )
    else:
        # No primary user to backfill to; leave column nullable so the
        # migration does not fail. Revisit after the user exists.
        raise RuntimeError(
            f"Primary user '{PRIMARY_USER_EMAIL}' not found; aborting to avoid "
            "adding a NOT NULL column with null rows. Register that user first."
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('fk_budgets_user_id_users'), 'budgets', type_='foreignkey')
    op.drop_column('budgets', 'user_id')
