from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from datetime import datetime,timezone
from app.schemas import CommentCreateRequest, CommentListResponse, CommentUpdateRequest
from app.models import Comments
from app.database import db_deb


router = APIRouter(prefix="/comment", tags=["Comment"])


@router.post("/create/", response_model=CommentListResponse)
async def comment_create(session: db_deb, create_data: CommentCreateRequest):
    comment = Comments(
        user_id=create_data.user_id, text=create_data.text, post_id=create_data.post_id
    )
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.get("/list/", response_model=list[CommentListResponse])
async def commnet_list(session: db_deb):
    stmt = select(Comments)
    res = session.execute(stmt).scalars().all()
    return res


@router.get("/one/", response_model=CommentListResponse)
async def comment_one(session: db_deb, comment_id: int):
    stmt = select(Comments).where(Comments.id == comment_id)
    res = session.execute(stmt).scalars().first()
    if not res:
        raise HTTPException(status_code=404, detail="comment not found")

    return res


@router.put("/update/", response_model=CommentListResponse)
async def comment_update(
    session: db_deb, update_data: CommentUpdateRequest, comment_id: int
):
    stmt = select(Comments).where(Comments.id == comment_id)
    res = session.execute(stmt).scalars().first()
    if not res:
        raise HTTPException(status_code=404, detail="not found comments")
    if update_data.text:
        res.text = update_data.text
    if update_data.post_id:
        res.post_id = update_data.post_id
    res.updated_at=datetime.now(timezone.utc)    
    session.commit()
    session.refresh(res)
    return res
@router.delete("/delete/")
async def comment_delete(session:db_deb,comment_id:int):
    stmt=select(Comments).where(Comments.id==comment_id)
    res=session.execute(stmt).scalars().first()
    if not res:
        raise HTTPException(status_code=404,detail="comment not found")
    session.delete(res)
    session.commit()
    return HTTPException(status_code=204,detail="comment deleted")


@router.put("/deactive/",response_model=CommentListResponse)
async def comment_deactive(session: db_deb,comment_id:int):
    stmt=select(Comments).where(Comments.id==comment_id)
    res=session.execute(stmt).scalars().first()
    if not res:
        raise HTTPException(status_code=404,detail="comment not found")
    res.is_active=False
    res.updated_at=datetime.now(timezone.utc)
    session.commit()
    session.refresh(res)
    return res