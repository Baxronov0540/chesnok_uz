from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_deb
from app.schemas import (
    PostCreateRequest,
    PostListResponse,
    session_auth_dep,
    CategoryCreateRequest,
    CategoryListResponse,
    CategoryUpdateRequest,
    current_user_jwt_dep
)
from app.models import Post, Category
from app.utils import generate_slug

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/post", response_model=PostListResponse)
async def post_create(
    db: db_deb, data: PostCreateRequest, current_user: session_auth_dep
):
    if not current_user.is_supperuser:
        raise HTTPException(status_code=403, detail="Sizda post qo'shishga huquq yuq")
    new_post = Post(
        title=data.title,
        body=data.body,
        user_id=current_user.id,
        category_id=data.category_id,
        slug=generate_slug(data.title),
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/post", response_model=list[PostListResponse])
async def get_post(session: db_deb, current_user: current_user_jwt_dep):
    if not current_user.is_supperuser:
        raise HTTPException(status_code=403, detail="sizda huquq yuq")

    stmt = select(Post)
    post = session.execute(stmt).scalars()
    return post


@router.delete("/post", status_code=204)
async def post_delete(session: db_deb, post_id: int, current_user: current_user_jwt_dep):
    if not current_user.is_supperuser:
        raise HTTPException(status_code=403, detail="sizda huquq yuq!!")

    stmt = select(Post).where(Post.id == post_id)
    post = session.execute(stmt).scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    session.delete(post)
    session.commit()


@router.post("/category", response_model=CategoryListResponse)
async def category_create(
    session: db_deb, current_user: session_auth_dep, data: CategoryCreateRequest
):
    if not current_user.is_supperuser:
        raise HTTPException(
            status_code=403, detail="Sizda create qilish uchun   huquq yuq!!"
        )

    new_category = Category(name=data.name, slug=generate_slug(data.name))

    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category


@router.get("/category", response_model=list[CategoryListResponse])
async def get_category(session: db_deb, current_user: session_auth_dep):
    if not current_user.is_supperuser:
        raise HTTPException(status_code=403, detail="sizda huquq yuq !!")

    stmt = select(Category)
    category = session.execute(stmt).scalars().all()

    return category


@router.delete("/category", status_code=204)
async def delete_category(
    session: db_deb, category_id: int, current_user: session_auth_dep
):
    if not current_user.is_supperuser:
        raise HTTPException(status_code=403, detail="sizda huquq yuq!!")
    stmt = select(Category).where(Category.id == category_id)
    res = session.execute(stmt).scalars().first()
    if not res:
        raise HTTPException(status_code=404, detail="category not found")

    session.delete(res)
    session.commit()


@router.put("/category", response_model=CategoryListResponse)
async def category_update(
    session: db_deb,
    update_data: CategoryUpdateRequest,
    current_user: session_auth_dep,
    category_id: int,
):
    if not current_user.is_supperuser:
        raise HTTPException(status_code=403, detail="sizda huquq yuq")


    stmt = select(Category).where(Category.id == category_id)
    res = session.execute(stmt).scalars().first()

    if not res:
        raise HTTPException(status_code=404, detail="Category not found")
    res.name = update_data.name
    res.slug = generate_slug(update_data.name)

    session.commit()
    session.refresh(res)

    return res
