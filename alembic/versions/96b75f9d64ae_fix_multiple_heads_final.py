"""fix_multiple_heads_final

Revision ID: 96b75f9d64ae
Revises: 64e5dcaaeed8, caac5e7815f2
Create Date: 2026-01-30 18:57:39.565886

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "96b75f9d64ae"
down_revision: Union[str, None] = ("64e5dcaaeed8", "caac5e7815f2")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
