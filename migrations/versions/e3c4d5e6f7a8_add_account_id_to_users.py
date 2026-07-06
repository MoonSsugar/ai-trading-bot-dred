"""add account_id to users

Revision ID: e3c4d5e6f7a8
Revises: d2b3c4d5e6f7
Create Date: 2026-07-06 19:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e3c4d5e6f7a8'
down_revision: Union[str, Sequence[str], None] = 'd2b3c4d5e6f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('account_id', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'account_id')
