from fastapi import APIRouter, Depends,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Post
from app.database import db_deb
from app.schemas import PostCreateRequest,PostListResponse,PostUpdateRequest
from app.utils import *
router=APIRouter(prefix="/posts",tags=["Posts"])

@router.get("/",response_model=list[PostListResponse])
async def get_posts(session:db_deb,is_active:bool = None):
    stmt=select(Post)
    if is_active is not None:
        stmt=stmt.where(Post.is_active==is_active)
    stmt=stmt.order_by(Post.created_at.desc())
    res=session.execute(stmt)
    return res.scalars().all()    
@router.post("/create",response_model=PostListResponse)
async def post_create(session:db_deb,
    create_data:PostCreateRequest):
    post=Post(
        title=create_data.title,
        body=create_data.body,
        slug=generate_slug(create_data.title),
        category_id=create_data.category_id
        
    )
    session.add(post)
    session.commit()
    session.refresh(post)

    return post
@router.get("/get/list")
async def get_list(session:db_deb,):

    stmt=select(Post).order_by(Post.created_at.desc())
    res=session.execute(stmt)
    res=res.scalars()

    return res.all()
@router.put("/update/{post_id}/title",response_model=PostListResponse)
def update_title(session:db_deb,post_id: int, update_data:PostUpdateRequest):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt).scalar_one_or_none()
    res.title=update_data.title
    res.body=update_data.body
    session.commit()
    session.refresh(res)

    if not res:
        raise HTTPException(status_code=404, detail="Post topilmadi")

    return res
@router.delete("/delete/{post_id}/")
async def post_delete(session:db_deb,post_id:int):
    stmt=select(Post).where(Post.id==post_id)
    res=session.execute(stmt).scalar_one_or_none()
    if not res:
        return JSONResponse(status_code=404)
    session.delete(res)
    session.commit()
@router.get("/get/{post_id}/",response_model=PostListResponse)
async def post_one(session:db_deb,post_id:int):
    stmt=select(Post).where(Post.id==post_id)
    res=session.execute(stmt).scalar_one_or_none()
    if not res:
        return JSONResponse(content={"detail": "Post topilmadi"},status_code=404)
    
    return res

@router.put("/deactive",response_model=PostListResponse)
async def post_deactive(session:db_deb,post_id:int):
    stmt=session.get(Post,post_id)
    if not stmt:
        return JSONResponse(status_code=404,content="{message:not found}")
    stmt.is_active=False
    session.commit()
    session.refresh(stmt)
    return stmt  