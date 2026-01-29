"""sdsfdf

Revision ID: 86078b27c891
Revises:
Create Date: 2026-01-24 20:40:51.532648

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "86078b27c891"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass 

def downgrade() -> None:
    pass
    # ### end Alembic commands ###
