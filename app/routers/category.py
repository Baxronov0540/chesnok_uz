from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.database import db_deb
from app.models import Category
from app.schemas import CategoryCreateRequest,CategoryListResponse,CategoryUpdateRequest
from app.utils import *

router=APIRouter(prefix="/category",tags=["Category"])

@router.post("/create",response_model=CategoryListResponse)

async def create_category(session:db_deb,create_data:CategoryCreateRequest):
   
    if not create_data:
        return JSONResponse(status_code=200)
    
    category=Category(name=create_data.name,
                      slug=generate_slug(create_data.name))
    session.add(category)
    session.commit()
    session.refresh(category)

    return category

@router.get("/list",response_model=list[CategoryListResponse])

async def category_list(session:db_deb):
    
    stmt=select(Category)
    res=session.execute(stmt).scalars().all()
    
    if res:
        return res
    return JSONResponse(status_code=404,content="{Message:Not found}")

@router.put("/update",response_model=CategoryListResponse)

async def category_update(session:db_deb,category_id:int,update_data:CategoryUpdateRequest):
    
    res=session.get(Category,category_id)
    
    if update_data.name:
        if not res:
            return JSONResponse(status_code=404,content="{message:not found}")
        res.name=update_data.name
        res.slug=generate_slug(update_data.name)
        session.commit()
        session.refresh(res)
        return res
    return res
@router.delete("/delete/{category_id}/")

async def category_delete(session:db_deb,category_id:int):
    
    stmt=session.get(Category,category_id)
    
    if not stmt:
        return JSONResponse(status_code=404,content="{message:not found}")
    session.delete(stmt)
    session.commit()
    return JSONResponse(status_code=204,content="deleted")

@router.get("one/{category_id}/",response_model=CategoryListResponse)

async def category_one(session:db_deb,category_id:int):
    
    stmt=session.get(Category,category_id)
    
    if not stmt:
        return JSONResponse(status_code=404,content="{message:not found}")
    return stmt

@router.get("/search")

async def search_get(session:db_deb,item:str):

    stmt=select(Category).where(Category.slug.ilike(f"%{item}%"))
    res=session.execute(stmt).scalars().first()
    if  not res:
        return JSONResponse(status_code=404,content="{message:not found}")
    post=[post.id for post in res.posts]
    return {"id":res.id,
            "name":res.name,
            "post":post}

