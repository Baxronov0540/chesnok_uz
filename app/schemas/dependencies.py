from datetime import datetime, timezone

from typing import Annotated
from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.database import db_deb
from app.models import User, UserSessionToken
from app.utils import verify_password

basic = HTTPBasic()
basic_auth_dep = Annotated[HTTPBasicCredentials, Depends(basic)]


def get_current_user(session: db_deb, credentials: basic_auth_dep):
    stmt = (
        select(User)
        .options(joinedload(User.proffesion))
        .where(User.email == credentials.username)
    )
    user = session.execute(stmt).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user


current_user_basic_dep = Annotated[User, Depends(get_current_user)]


###Session Auth


def get_current_user_session(session: db_deb, request: Request):
    sessionId = request.cookies.get("sessionId")
    stmt = select(UserSessionToken).where(UserSessionToken.token == sessionId)
    session_obj = session.execute(stmt).scalars().first()

    print(sessionId)
    if not session_obj:
        print("msldm")
        raise HTTPException(status_code=401, detail="Not authenticated")

    if session_obj.expires_at < datetime.now(timezone.utc):
        session.delete(session_obj)
        session.commit()
        raise HTTPException(status_code=401, detail=" Not authenticated")

    stmt = (
        select(User)
        .options(joinedload(User.proffesion))
        .where(User.id == session_obj.user_id)
    )
    user = session.execute(stmt).scalars().first()
    if not user or user.is_deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return user


session_auth_dep = Annotated[User, Depends(get_current_user_session)]
