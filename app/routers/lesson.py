from fastapi import APIRouter, Header, HTTPException
from typing import Annotated
from sqlalchemy import select
from app.database import db_deb
from app.models import User


router = APIRouter(prefix="/lesson", tags=["Lesson"])
SECRET_TOKEN = "asror"


@router.get("/protected/")
async def protected_api(
    db: db_deb, email: str, X_chesnok_token: Annotated[str | None, Header()] = None
):#noqa
    if not X_chesnok_token:
        raise HTTPException(status_code=401, detail="no chesnok Token ")

    if SECRET_TOKEN != X_chesnok_token:
        raise HTTPException(status_code=401, detail="INCORRECT  chesnok TOKEN")

    stmt = select(User).where(User.email == email)
    res = db.execute(stmt)
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return res


@router.get("/protected/admin/")
async def protected_api(
    db: db_deb, email: str, X_chesnok_token: Annotated[str | None, Header()] = None
):
    if not X_chesnok_token:
        raise HTTPException(status_code=401, detail="no chesnok Token ")

    if SECRET_TOKEN != X_chesnok_token:
        raise HTTPException(status_code=401, detail="INCORRECT  chesnok TOKEN")

    stmt = select(User).where(User.email == email)
    res = db.execute(stmt)
    user = res.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_supperuser:
        raise HTTPException(status_code=403, detail="San mani adminim emassan")

    return user
