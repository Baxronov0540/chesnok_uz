from .posts import router as posts_router
from .tag import router as tags_router
from .category import router as category_router
from .proffesion import router as proffesion_router
from .post_tag import router as post_tag_router
from .user import router as user_router
from .comment import router as comment_router
from .user_search import router as user_search_router

__all__ = [
    "posts_router",
    "tags_router",
    "category_router",
    "proffesion_router",
    "post_tag_router",
    "user_router",
    "comment_router",
]
