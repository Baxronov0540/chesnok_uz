from fastapi import APIRouter ,HTTPException,Depends
from typing import Annotated
from sqlalchemy import select
from fastapi.security import HTTPBasic,HTTPBasicCredentials

from app.models import User
from app.database import db_deb
from app.schemas import UserRegisterRequest,UserRegisterResponse,UserProfileResponse
from app.utils import hash_password
from app.utils import verify_password

basic=HTTPBasic()
router=APIRouter(prefix="/auth",tags=["Authintication"])


@router.post("/register/",response_model=UserRegisterResponse)
async def  register_user(db:db_deb,data:UserRegisterRequest):
    stmt=select(User).where(User.email==data.email)
    res=db.execute(stmt).scalars().first()
    if res:
        raise HTTPException(status_code=404,detail="User already exsists")
    user=User(email=data.email,
              password_hash=hash_password(data.password))
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
@router.post("/login-user/",)
async def login_user(db:db_deb,credintials:Annotated[HTTPBasicCredentials,Depends(basic)]):
    stmt=select(User).where(User.email==credintials.username)
    res=db.execute(stmt).scalars().first()

    if not res:
        raise HTTPException(status_code=404,detail="User not found")

    if not verify_password(credintials.password,res.password_hash):
        raise HTTPException(status_code=401,detail="Incorrect password")
    return res


@router.get("/profile",response_model=UserProfileResponse)
async def user_profile(db:db_deb,credintials:Annotated[HTTPBasicCredentials,Depends(basic)]):
    stmt=select(User).where(User.email==credintials.username)
    res=db.execute(stmt).scalars().first()
    if not res:
        raise HTTPException(status_code=404,detail="User not found")
    if not verify_password(credintials.password,res.password_hash):
        raise HTTPException(status_code=401,detail="Incorect password")
    return res











    
