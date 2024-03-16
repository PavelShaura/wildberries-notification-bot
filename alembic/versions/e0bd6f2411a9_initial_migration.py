"""Initial migration

Revision ID: e0bd6f2411a9
Revises:
Create Date: 2024-03-16 09:27:20.650187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e0bd6f2411a9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'queries',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.BigInteger),
        sa.Column('timestamp', sa.DateTime),
        sa.Column('product_code', sa.String),
    )


def downgrade():
    op.drop_table('queries')
