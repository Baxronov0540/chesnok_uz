from fastapi import FastAPI

from app.models import *

from app.routers import posts_router
from app.routers import tags_router
from app.routers import category_router
from app.routers import proffesion_router
from app.routers import post_tag_router
from app.routers import user_router
from app.routers import comment_router

app = FastAPI(
    title="Chesnokdan achiq haqiqatlar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI",
)

app.include_router(posts_router)
app.include_router(tags_router)
app.include_router(category_router)
app.include_router(proffesion_router)
app.include_router(post_tag_router)
app.include_router(user_router)
app.include_router(comment_router)
