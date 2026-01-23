from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import *

from app.utils import generate_slug
from app.schemas import  PostCreateRequest,PostListResponse,PostUpdateRequest

app=FastAPI(
    title="Chesnokdan achiq haqiqatlar",
    description="Chesnokuz - news website inspired from Qalampir.uz, built in FastAPI"

)


@app.post("/post/create",response_model=PostListResponse)
async def post_create(
    create_data:PostCreateRequest,session:Session=Depends(get_db)):
    post=Post(
        title=create_data.title,
        body=create_data.body,
        slug=generate_slug(create_data.title)
    )
    session.add(post)
    session.commit()
    session.refresh(post)

    return post
@app.get("/get/list")
async def get_list(sesssion:Session=Depends(get_db)):

    stmt=select(Post).order_by(Post.created_at.desc())
    res=sesssion.execute(stmt)
    res=res.scalars()

    return res.all()
@app.put("/update/{post_id}/title",response_model=PostListResponse)
def update_title(post_id: int, update_data:PostUpdateRequest,session: Session = Depends(get_db)):
    stmt = select(Post).where(Post.id == post_id)
    res = session.execute(stmt).scalar_one_or_none()
    res.title=update_data.title
    res.body=update_data.body
    session.commit()
    session.refresh(res)

    if not res:
        raise HTTPException(status_code=404, detail="Post topilmadi")

    return res

@app.delete("/delete/{post_id}/")
async def post_delete(post_id:int,session:Session=Depends(get_db)):
    stmt=select(Post).where(Post.id==post_id)
    res=session.execute(stmt).scalar_one_or_none()
    if not res:
        return JSONResponse(status_code=404)
    session.delete(res)
    session.commit()
@app.get("/get/{post_id}/",response_model=PostListResponse)
async def post_one(post_id:int,session:Session=Depends(get_db)):
    stmt=select(Post).where(Post.id==post_id)
    res=session.execute(stmt).scalar_one_or_none()
    if not res:
        return JSONResponse(content={"detail": "Post topilmadi"},status_code=404)
    
    return res

@app.get("/get/query")
async def query_parametr(q:bool,session:Session=Depends(get_db)):
    stmt=select(Post)
    if stmt is not None:
     stmt=stmt.where(Post.is_active==q)
    stmt=stmt.order_by(Post.created_at.desc())
    res=session.execute(stmt)
    return res.scalars().all()
