"""create channels table

Revision ID: baee7ff7eb83
Revises: 
Create Date: 2024-02-07 11:57:59.982091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'baee7ff7eb83'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "channels",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("telegram_chat_id", sa.BigInteger, nullable=False, unique=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("username", sa.String(100), nullable=True)
    )


def downgrade() -> None:
    op.drop_table("channels")
