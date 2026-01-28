"""empty message

Revision ID: fef57b490207
Revises: 86078b27c891
Create Date: 2026-01-28 11:16:49.407237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fef57b490207'
down_revision: Union[str, None] = '86078b27c891'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import DateTime, func

def upgrade() -> None:
    # 1️⃣ is_active ustunini qo'shish (default bilan)
    op.add_column(
        'comments',
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true())
    )

    # 2️⃣ created_at va updated_at ustunlarini qo'shish (dastlab nullable=True)
    op.add_column(
        'comments',
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        'comments',
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True)
    )

    # 3️⃣ Eski yozuvlarni NOW() bilan to‘ldirish
    comments_table = table('comments',
        column('created_at', DateTime),
        column('updated_at', DateTime)
    )

    op.execute(
        comments_table.update().values(
            created_at=func.now(),
            updated_at=func.now()
        )
    )

    # 4️⃣ Keyin NOT NULL qilib qo‘yish

def downgrade() -> None:
    op.drop_column('comments', 'updated_at')
    op.drop_column('comments', 'created_at')
    op.drop_column('comments', 'is_active')
