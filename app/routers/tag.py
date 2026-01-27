from fastapi import APIRouter,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.models import Tag
from app.database import db_deb
from app.schemas import TagCreateRequest, TagListResponse, TagUpdateRequest
from app.utils import *

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("/create", response_model=TagListResponse)
async def create_tag(session: db_deb, create_data: TagCreateRequest):
    tag = Tag(name=create_data.name, slug=generate_slug(create_data.name))
    session.add(tag)
    session.commit()
    session.refresh(tag)

    return tag


@router.get("/list", response_model=list[TagListResponse])
async def tag_list(session: db_deb):
    stmt = select(Tag)
    res = session.execute(stmt)
    tag = res.scalars().all()

    return tag


@router.put("/update", response_model=TagListResponse)
async def update_tag(session: db_deb, update_data: TagUpdateRequest, tag_id: int):
    stmt = select(Tag).where(Tag.id == tag_id)
    res = session.execute(stmt).scalars().first()
    if res:
     res.name = update_data.name
     res.slug = generate_slug(update_data.name)
     session.commit()
     session.refresh(res)
     return res
    raise HTTPException(status_code=404, detail="not found")


@router.delete("/delete/{tag_id}/")
async def tag_delete(session: db_deb, tag_id: int):
    stmt = select(Tag).where(Tag.id == tag_id)
    res = session.execute(stmt).scalars().first()

    if res:
        session.delete(res)
        session.commit()
        return HTTPException(status_code=204, detail="deleted")
    raise HTTPException(status_code=404, detail="not found")


@router.get("/get/{tag_id}/", response_model=TagListResponse)
async def one_tag(session: db_deb, tag_id: int):
    stmt = session.get(Tag, tag_id)

    if not stmt:
        raise HTTPException(status_code=404, detail="not found")
    return stmt


@router.get("/posttag")
async def post_tag(session: db_deb, tag_id: int):
    stmt = session.get(Tag, tag_id)
    if not stmt:
        raise HTTPException(status_code=404, detail="post tag not found")
    post = [post.post.title for post in stmt.post_tags]
    return {"tag_id": stmt.id, "tag_name": stmt.name, "post_title": post}
