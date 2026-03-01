import shutil

from pathlib import Path

from fastapi import APIRouter, Header, HTTPException,Form,Depends,UploadFile,File
from typing import Annotated
from sqlalchemy import select
from app.database import db_deb
from app.models import User,Media
from app.config import settings
from app.schemas import AnasbekSleepingException


router = APIRouter(prefix="/lesson", tags=["Lesson"])
SECRET_TOKEN = "asror"


@router.get("/protected/")
async def protected_api(
    db: db_deb, email: str, X_chesnok_token: Annotated[str | None, Header()] = None
):  # noqa
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




@router.post("/testlogin")
async def test_login(username:Annotated[str,Form()],password:Annotated[str,Form()]):
    return {"username":username,"password":password}

@router.post("/uploadfile")
async def create_uploadfile(db:db_deb,file:UploadFile):


    file_ext=Path(file.filename).suffix.lower()

    if file.size >1024*1024*1:
        HTTPException(status_code=400,detail="file size maxs size 1 mb")
    
    if file_ext not in  [".jpg",".png",".jpeg"]:
        raise HTTPException(status_code=400, detail="File type is not supported. Only .jpg , .png , .jpeg  ")

    path=Path(settings.MEDIA_PATH)
    path.mkdir(exist_ok=True)
    res=path/file.filename
    with open(res,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)

    image=Media(
        url=f"{settings.MEDIA_PATH}/{file.filename}"

    )
    db.add(image)
    db.commit()
    db.refresh(image)

    return f"filename:{image.id},res:{image.url}"
@router.get("/zero")
async def zero():
    raise ZeroDivisionError("nolga bo'lish mumkin emas")

@router.get("/exception")
async def sleep():
    raise AnasbekSleepingException("uxlama!!")

