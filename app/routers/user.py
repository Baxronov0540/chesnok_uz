from fastapi import APIRouter, Response, Cookie
from fastapi import HTTPException
from enum import Enum
from sqlalchemy import select

from app.database import db_deb
from app.models import User
from app.schemas import (
    UserListResponse,
    UserCreateRequest,
    UserUpdateRequest,
    CookieData,
)
from app.utils import *

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/create/", response_model=UserListResponse)
async def user_create(session: db_deb, create_data: UserCreateRequest):
    user = User(
        proffesion_id=create_data.proffesion_id,
        email=create_data.email,
        avatar_id=create_data.avatar_id,
        password_hash=create_data.password_hash,
        first_name=create_data.first_name,
        last_name=create_data.last_name,
        bio=create_data.bio,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/list/", response_model=list[UserListResponse])
async def user_list(session: db_deb):
    stmt = select(User)
    res = session.execute(stmt).scalars().all()

    return res


@router.get("/one/", response_model=UserListResponse)
async def one_user(session: db_deb, user_id: int):
    stmt = select(User).where(User.id == user_id)
    res = session.execute(stmt).scalars().first()
    if not res:
        raise HTTPException(status_code=404, detail="user not found")
    return res


@router.put("/update/", response_model=UserListResponse)
async def user_update(session: db_deb, update_data: UserUpdateRequest, user_id: int):
    stmt = select(User).where(User.id == user_id)
    res = session.execute(stmt).scalars().first()
    if update_data.avatar_id:
        res.avatar_id = update_data.avatar_id
    if update_data.email:
        res.email = update_data.email
    if update_data.first_name:
        res.first_name = update_data.first_name
    if update_data.is_active:
        res.is_active = update_data.is_active
    if update_data.is_staff:
        res.is_staff = update_data.is_staff
    if update_data.is_supperuser:
        res.is_supperuser = update_data.is_supperuser
    if update_data.last_name:
        res.last_name = update_data.last_name
    if update_data.bio:
        res.bio = update_data.bio
    session.commit()
    session.refresh(res)
    return res


@router.delete("/delete/", response_model=UserListResponse)
async def user_delete(session: db_deb, user_id: int):
    stmt = select(User).where(User.id == user_id)
    res = session.execute(stmt).scalars().first()
    if not res:
        raise HTTPException(status_code=404, detail="user not found")
    session.delete(res)
    session.commit()
    return HTTPException(status_code=204, detail="user deleted")


@router.get("/filter/created_at/", response_model=list[UserListResponse])
async def filter_created_at(session: db_deb):
    stmt = select(User).order_by(User.created_at.desc())
    res = session.execute(stmt).scalars().all()
    return res


@router.get("/is_active/", response_model=list[UserListResponse])
async def filter_is_active(session: db_deb, q: bool):
    stmt = select(User)
    if not session.execute(stmt).all():
        return HTTPException(status_code=404, detail="user not found")

    stmt = stmt.where(User.is_active == q)
    res = session.execute(stmt).scalars().all()
    return res


@router.post("/set-cookie/")
def set_cookie(data: CookieData, response: Response):
    response.set_cookie(key=data.key, value=data.value, httponly=True, max_age=60 * 60)
    return {"message": "Cookie saqlandi"}


@router.get("/get-cookie/")
def get_cookie(user_token: str | None = Cookie(default=None)):
    if not user_token:
        return {"message": "Cookie topilmadi"}
    return {"user_token": user_token}


@router.delete("/delete-cookie/")
def delete_cookie(response: Response):
    response.delete_cookie("user_token")
    return {"message": "Cookie o‘chirildi"}


class ThemeEnum(str, Enum):
    LIGHT = "light"
    DARK = "dark"


from fastapi import APIRouter, Response
from enum import Enum


class ThemeEnum(str, Enum):
    LIGHT = "light"
    DARK = "dark"


@router.post("/theme/set")
def set_theme(theme: ThemeEnum, response: Response):
    # Cookie ga o'rnatish
    response.set_cookie(
        key="theme", value=theme.value, max_age=60 * 60 * 24 * 30, httponly=False
    )
    return {"message": f"Tema {theme.value} ga o‘rnatildi"}


@router.get("/theme/get")
def get_theme(theme: str = Cookie(default="light")):
    return {"theme": theme}
