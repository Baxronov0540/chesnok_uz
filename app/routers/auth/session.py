import secrets
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException, Response
from sqlalchemy import select

from app.database import db_deb
from app.models import UserSessionToken, User
from app.schemas import (
    session_auth_dep,
    UserLoginRequest,
    UserProfileResponse,
    UserProfilUpdateRequest,
)
from app.utils import verify_password
from app.config import settings


router = APIRouter(prefix="/session", tags=["Auth"])


@router.post("/login/", status_code=200)
async def login(db: db_deb, login_data: UserLoginRequest, response: Response):
    stmt = select(User).where(User.email == login_data.email)
    user = db.execute(stmt).scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    sessionId = secrets.token_hex(32)
    new_session = UserSessionToken(
        token=sessionId,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc)
        + timedelta(days=settings.SESSION_ID_EXPIRE_DAYS),
    )
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    response.set_cookie(
        key="sessionId",
        value=sessionId,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.SESSION_ID_EXPIRE_DAYS * 24 * 60 * 60,
    )


@router.get("/profil/", response_model=UserProfileResponse)
async def get_porfil(current_user: session_auth_dep):
    return current_user


@router.put("/update/", response_model=UserProfileResponse)
async def profil_update(
    session: db_deb,
    update_data: UserProfilUpdateRequest,
    current_user: session_auth_dep,
):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    if update_data.proffession_id:
        current_user.proffesion_id = update_data.proffession_id

    session.commit()
    session.refresh(current_user)
    return current_user


@router.get("/logout/")
async def profil_logout(session: db_deb, current_user: session_auth_dep):
    stmt = select(UserSessionToken).where(UserSessionToken.user_id == current_user.id)
    token = session.execute(stmt).scalars().first()
    if token:
        session.delete(token)
        session.commit()
