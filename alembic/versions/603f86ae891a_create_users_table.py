"""create users table

Revision ID: 603f86ae891a
Revises: ec7d8c70af8d
Create Date: 2024-02-07 16:59:54.193354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '603f86ae891a'
down_revision: Union[str, None] = 'ec7d8c70af8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('telegram_user_id', sa.BigInteger, nullable=False),
        sa.Column('username', sa.String(100), nullable=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('channel_id', sa.Integer, sa.ForeignKey("channels.id"), nullable=True),
        sa.Column('distribution_id', sa.Integer, sa.ForeignKey("distributions.id"), nullable=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("users")
