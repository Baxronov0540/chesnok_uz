"""merge multiple heads

Revision ID: 64e5dcaaeed8
Revises: 02503f782224
Create Date: 2026-01-30 18:51:38.567707

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "64e5dcaaeed8"
down_revision: Union[str, None] = "02503f782224"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
