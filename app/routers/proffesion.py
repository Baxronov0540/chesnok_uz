from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy import select

from app.database import db_deb
from app.models import Proffesion
from app.schemas import ProffesionCreateRequest,ProffesionListResponse,ProffesionUpdateRequest
from app.utils import *

router=APIRouter(prefix="/proffesion",tags=["Proffesion"])

@router.post("/create",response_model=ProffesionListResponse)

async def create_proffesion(session:db_deb,create_data:ProffesionCreateRequest):
    
    proffesion=Proffesion(name=create_data.name)
    session.add(proffesion)
    session.commit()
    session.refresh(proffesion)
    return proffesion

@router.get("/list",response_model=list[ProffesionListResponse])

async def proffesion_list(session:db_deb):
    
    stmt=select(Proffesion)
    res=session.execute(stmt).scalars().all()
    
    if not res:
        return JSONResponse(status_code=404,content="{message:not found}")
    return res

@router.put("/update",response_model=ProffesionListResponse)


async def proffesion_update(session:db_deb,proffesion_id:int,update_data:ProffesionUpdateRequest):
         
         stmt=session.get(Proffesion,proffesion_id)
         
         if update_data.name:
              if not stmt:
                   return JSONResponse(status_code=404,content="{message:Not found}")
              stmt.name=update_data.name
              session.commit()
              session.refresh(stmt)
              return     stmt
         return stmt

@router.delete("/delete/{proffesion_id}/")

async def proffesion_delete(session:db_deb,proffesion_id:int):
     
     stmt=session.get(Proffesion,proffesion_id)
     
     if not stmt:
          return JSONResponse(status_code=404,content="{message:not found}")
     session.delete(stmt)
     session.commit()
     return JSONResponse(status_code=204,content="{message:deleted}")


