"""add distribution info

Revision ID: 1e9a2d627f9c
Revises: 603f86ae891a
Create Date: 2024-02-14 10:02:12.458051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e9a2d627f9c'
down_revision: Union[str, None] = '603f86ae891a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('distribution_sent', sa.Boolean, default=False))
    op.add_column('users', sa.Column('distribution_date', sa.DateTime, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'distribution_sent')
    op.drop_column('users', 'distribution_date')
