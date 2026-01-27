from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.database import db_deb
from app.models import PostTag
from app.schemas import PostTagCreateRequest, PostTagListResponse
from app.utils import *

router = APIRouter(prefix="/post_tag", tags=["PostTag"])


@router.post("/create", response_model=PostTagListResponse)
async def post_tag_create(session: db_deb, create_data: PostTagCreateRequest):
    if not create_data.post_id or not create_data.tag_id:
        return JSONResponse(
            status_code=200, content="{message: create_datada malumot yuq}"
        )
    post_tag = PostTag(post_id=create_data.post_id, tag_id=create_data.tag_id)
    session.add(post_tag)
    session.commit()
    session.refresh(post_tag)
    return post_tag
