from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_deb
from app.models import Category
from app.schemas import (
    CategoryCreateRequest,
    CategoryListResponse,
    CategoryUpdateRequest,
)
from app.utils import *

router = APIRouter(prefix="/category", tags=["Category"])


@router.post("/create", response_model=CategoryListResponse)
async def create_category(session: db_deb, create_data: CategoryCreateRequest):
    category = Category(name=create_data.name, slug=generate_slug(create_data.name))
    session.add(category)
    session.commit()
    session.refresh(category)

    return category


@router.get("/list", response_model=list[CategoryListResponse])
async def category_list(session: db_deb):
    stmt = select(Category)
    res = session.execute(stmt).scalars().all()

    return res


@router.put("/update", response_model=CategoryListResponse)
async def category_update(
    session: db_deb, category_id: int, update_data: CategoryUpdateRequest
):
    res = session.get(Category, category_id)

    if res:
        res.name = update_data.name
        res.slug = generate_slug(update_data.name)
        session.commit()
        session.refresh(res)
        return res
    raise HTTPException(status_code=404, detail="not found")


@router.delete("/delete/{category_id}/")
async def category_delete(session: db_deb, category_id: int):
    stmt = session.get(Category, category_id)

    if not stmt:
        raise HTTPException(status_code=404, detail="not found")
    session.delete(stmt)
    session.commit()
    return HTTPException(status_code=204, detail="deleted")


@router.get("one/{category_id}/", response_model=CategoryListResponse)
async def category_one(session: db_deb, category_id: int):
    stmt = session.get(Category, category_id)

    if not stmt:
        raise HTTPException(status_code=404, content="not found")
    return stmt


@router.get("/search")
async def search_get(session: db_deb, item: str):
    stmt = select(Category).where(Category.slug.ilike(f"%{item}%"))
    res = session.execute(stmt).scalars().first()
    if not res:
        raise HTTPException(status_code=404, content="not found")
    post = [post.id for post in res.posts]
    return {"id": res.id, "name": res.name, "post": post}
