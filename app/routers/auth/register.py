from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from fastapi.security import HTTPBasic

from app.models import User
from app.database import db_deb
from app.schemas import UserRegisterRequest, UserRegisterResponse
from app.utils import hash_password

basic = HTTPBasic()
router = APIRouter(prefix="/register", tags=["Auth"])


@router.post("/", response_model=UserRegisterResponse)
async def register_user(db: db_deb, data: UserRegisterRequest):
    stmt = select(User).where(User.email == data.email)
    res = db.execute(stmt).scalars().first()
    if res:
        raise HTTPException(status_code=404, detail="User already exsists")
    user = User(email=data.email, password_hash=hash_password(data.password))
    stmt = select(User)
    exsisting_user = db.execute(stmt).scalars().first()
    if not exsisting_user:
        user.is_staff = True
        user.is_supperuser = True

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
