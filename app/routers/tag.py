from fastapi import APIRouter, Depends,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select,delete
from sqlalchemy.orm import Session

from app.models import Tag
from app.database import db_deb
from app.schemas import TagCreateRequest,TagListResponse,TagUpdateRequest
from app.utils import *
router=APIRouter(prefix="/tags",tags=["Tags"])

@router.post("/create",response_model=TagListResponse)
async def create_tag(session:db_deb,create_data:TagCreateRequest):

    tag=Tag(name=create_data.name,
            slug=generate_slug(create_data.name))
    session.add(tag)
    session.commit()
    session.refresh(tag)

    return tag

@router.get("/list",response_model=list[TagListResponse])
async def tag_list(session:db_deb):
    stmt=select(Tag)
    res=session.execute(stmt)
    tag=res.scalars().all()
    if not tag:
        return JSONResponse(status_code=404)
    return tag
@router.put("/update",response_model=TagListResponse)
async def update_tag(session:db_deb,update_data:TagUpdateRequest,tag_id:int):
    stmt=select(Tag).where(Tag.id==tag_id)
    res=session.execute(stmt).scalars().first()
    if  res :
        if update_data.name:
           
          res.name=update_data.name
          res.slug=generate_slug(update_data.name)
        return res
    return JSONResponse(status_code=404,content={"message": "Tag not found"} )
@router.delete("/delete/{tag_id}/")
async def tag_delete(session:db_deb,tag_id:int):
    
     stmt=select(Tag).where(Tag.id==tag_id)
     res=session.execute(stmt).scalars().first()
     if res:
      session.delete(res)
      session.commit()
      return JSONResponse(status_code=204,content="deleted")
     return JSONResponse(status_code=404,content="not found") 
     
@router.get("/get/{tag_id}/",response_model=TagListResponse)
async def one_tag(session:db_deb,tag_id:int):
    stmt=session.get(Tag,tag_id)
    if not stmt:
        return JSONResponse(status_code=404,content="not found")
    return stmt

