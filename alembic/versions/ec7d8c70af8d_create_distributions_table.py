"""create distributions table

Revision ID: ec7d8c70af8d
Revises: baee7ff7eb83
Create Date: 2024-02-07 11:59:33.447864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec7d8c70af8d'
down_revision: Union[str, None] = 'baee7ff7eb83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "distributions",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("interval_measure", sa.String(100), nullable=True),
        sa.Column("interval_number", sa.Integer, nullable=True),
        sa.Column("interval_count", sa.Integer, nullable=True),
        sa.Column("text", sa.Text, nullable=False)
    )


def downgrade() -> None:
    op.drop_table("distribution")
