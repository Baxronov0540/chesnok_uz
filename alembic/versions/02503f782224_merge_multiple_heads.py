"""merge multiple heads

Revision ID: 02503f782224
Revises: 426c3b65f683, c55592854576
Create Date: 2026-01-30 18:51:30.197846

"""

from typing import Sequence, Union



# revision identifiers, used by Alembic.
revision: str = "02503f782224"
down_revision: Union[str, None] = ("426c3b65f683", "c55592854576")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
