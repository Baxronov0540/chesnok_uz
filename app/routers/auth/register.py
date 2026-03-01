import secrets
from fastapi import APIRouter, HTTPException,Request
from sqlalchemy import select
from fastapi.security import HTTPBasic
from fastapi.responses import JSONResponse
import redis

from app.models import User
from app.database import db_deb
from app.schemas import UserRegisterRequest, UserRegisterResponse
from app.utils import hash_password,send_email,redis_client
from app.limiter import limiter

basic = HTTPBasic()
router = APIRouter(prefix="/register", tags=["Auth"])


@router.post("/", response_model=UserRegisterResponse)
@limiter.limit("2/minute")
async def register_user(db: db_deb, data: UserRegisterRequest,request:Request):
    stmt = select(User).where(User.email == data.email)
    res = db.execute(stmt).scalars().first()
    if res:
        raise HTTPException(status_code=404, detail="User already exsists")
    user = User(email=data.email, password_hash=hash_password(data.password),is_active=False)
    
    code=secrets.token_hex(16)
    send_email(data.email,"email confirmation",f"Your confirmation code is {code}") 
    redis_client.setex(code,60,user.email)


    stmt = select(User)
    exsisting_user = db.execute(stmt).scalars().first()
    if not exsisting_user:
        user.is_staff = True
        user.is_supperuser = True

    db.add(user)
    db.commit()
    db.refresh(user)
    return JSONResponse(status_code=201,
                        content={"message":"Email confirmation sent to your email "})

@router.post("verify_eamil/{code}/",response_model=UserRegisterResponse)
async def verify_code(db:db_deb,code:str):

    email=redis_client.get(code)
    if not code :
        HTTPException(status_code=400,detail="Invalid code")
    stmt=select(User).where(User.email==email)
    user=db.execute(stmt).scalars().first()
    if not user :
        raise HTTPException(status_code=404,detail="User not found ")
    user.is_active=True
    db.commit()
    db.refresh(user)

    return user

