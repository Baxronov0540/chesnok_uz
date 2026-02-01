"""added_new_features

Revision ID: a5b8695426fd
Revises: e877126e478b
Create Date: 2026-01-30 19:09:17.581372

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a5b8695426fd"
down_revision: Union[str, None] = "e877126e478b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Agar ustun bazada bo'lsa, xato bermasligi uchun add_column ni izohga olamiz
    # yoki uni o'chirib tashlaymiz. Chunki ustun allaqachon bor.
    # op.add_column('posts', sa.Column('user_id', sa.BigInteger(), nullable=True))

    # 2. Hamma postlarga bitta user ID ni berib yuboramiz (masalan, ID=1 bo'lgan user)
    # Bazangizda ID=1 bo'lgan user borligiga ishonch hosil qiling
    op.execute("UPDATE posts SET user_id = 87 WHERE user_id IS NULL")

    # 3. ForeignKey bog'liqligini yaratamiz (agar u ham bo'lmasa)
    # Agar bu ham Duplicate xatosini bersa, buni ham izohga olasiz
    try:
        op.create_foreign_key("fk_posts_user_id", "posts", "users", ["user_id"], ["id"])
    except Exception:
        pass
