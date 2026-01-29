from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from datetime import datetime,timezone,timedelta

from app.models import Post,PostTag,Tag,User,UserSearch
from app.database import db_deb
from app.schemas import PostCreateRequest, PostListResponse, PostUpdateRequest
from app.utils import *

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostListResponse])
async def get_posts(session: db_deb, is_active: bool = None):
    stmt = select(Post)
    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)
    stmt = stmt.order_by(Post.created_at.desc())
    res = session.execute(stmt)
    return res.scalars().all()


@router.post("/create", response_model=PostListResponse)
async def post_create(session: db_deb, create_data: PostCreateRequest):
    post = Post(
        title=create_data.title,
        body=create_data.body,
        slug=generate_slug(create_data.title),
        category_id=create_data.category_id,
    )

    session.add(post)
    session.commit()
    session.refresh(post)

    return post


@router.get("/get/list/")
async def get_list(
    session: db_deb,
):
    stmt = select(Post).order_by(Post.created_at.desc())
    res = session.execute(stmt)
    res = res.scalars()

    return res.all()


@router.put("/update/{post_id}/title", response_model=PostListResponse)
def update_title(session: db_deb, post_id: int, update_data: PostUpdateRequest):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt).scalar_one_or_none()
    res.title = update_data.title
    res.body = update_data.body
    session.commit()
    session.refresh(res)

    if not res:
        raise HTTPException(status_code=404, detail="Post topilmadi")

    return res


@router.delete("/delete/{post_id}/")
async def post_delete(session: db_deb, post_id: int):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt).scalar_one_or_none()

    if not res:
        raise HTTPException(status_code=404, detail="user not found")
    session.delete(res)
    session.commit()
    return HTTPException(status_code=204, detail="user deleted")


@router.get("/get/{post_id}/", response_model=PostListResponse)
async def post_one(session: db_deb, post_id: int):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt).scalar_one_or_none()

    if not res:
        return JSONResponse(content={"detail": "Post topilmadi"}, status_code=404)

    return res


@router.put("/deactive", response_model=PostListResponse)
async def post_deactive(session: db_deb, post_id: int):
    stmt = session.get(Post, post_id)
    if not stmt:
        raise HTTPException(status_code=404, detail="post not found")

    stmt.is_active = False
    session.commit()
    session.refresh(stmt)
    return stmt


###filter


@router.get(
    "/search/",
    response_model=list[PostListResponse],
    summary="Postlarni sarlavha yoki slug bo‘yicha qidirish",
)
async def search_posts(session: db_deb, q: str):
    stmt = select(Post).where(Post.slug.like(f"%{q.lower()}%"))
    posts = session.execute(stmt).scalars().all()
    stmt1=select(UserSearch.term)
    res=session.execute(stmt1).scalars().all()
    flag=False
    if q in res:
        stmt2=select(UserSearch).where(UserSearch.term.ilike(f"{q}"))
        res=session.execute(stmt2).scalars().first()
        res.count+=1
        session.commit()
        session.refresh(res)
        flag=True

    if not flag:
        trenning=UserSearch(
            term=q,
            count=0
        )
        session.add(trenning)
        session.commit()
        session.refresh(trenning)
    return posts





@router.get("/created-at/filter/", response_model=list[PostListResponse])
async def get_posts_by_created_at(session: db_deb):
    stmt = select(Post).order_by(Post.created_at.desc())
    posts = session.execute(stmt).scalars().all()

    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")

    return posts



@router.get("/filter/", response_model=list[PostListResponse])
async def get_posts_list(
    session: db_deb,
    is_active: bool | None = None,
    category_id: int | None = None,
    tag_id: int | None = None,
):
    stmt = (
        select(Post)
        .join(PostTag, Post.id == PostTag.post_id)
        .join(Tag, PostTag.tag_id == Tag.id)
    )

    if is_active is not None:
        stmt = stmt.where(Post.is_active == is_active)

    if category_id:
        stmt = stmt.where(Post.category_id == category_id)

    if tag_id:
        stmt = stmt.where(Tag.id == tag_id)

    stmt = stmt.order_by(Post.created_at.desc())
    res = session.execute(stmt)
    return res.scalars().all()

@router.get("/filter/user/",response_model=PostListResponse)
async def user_filter(session:db_deb,user_id:int):
    stmt=select(Post).join(User,User.id==Post.user_id)
    if user_id:
        stmt=stmt.where(User.id==user_id)
        res=session.execute(stmt).scalars()
    return     res


@router.get("/trenning/",response_model=PostListResponse)
async def trenning_post(session:db_deb):
    stmt=select(Post).where(Post.created_at>=datetime.now(timezone.utc)-timedelta(days=7)).order_by(Post.likes_count.desc()).limit(5)
    res=session.execute(stmt)
    return res




