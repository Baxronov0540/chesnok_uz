from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_deb
from app.schemas import (
    UserLoginRequest,
    RefreshTokenRequest,
    UserProfileResponse,
    current_user_jwt_dep,
    UserProfilUpdateRequest,
)
from app.models import User
from app.utils import verify_password, generate_jwt_tokens, decode_jwt_token


router = APIRouter(prefix="/jwt", tags=["Auth"])


@router.post("/login")
async def login(session: db_deb, data: UserLoginRequest):
    stmt = select(User).where(User.email == data.email)
    user = session.execute(stmt).scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token, refresh_token = generate_jwt_tokens(user.id)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
async def refresh_token(session: db_deb, data: RefreshTokenRequest):
    decoded_data = decode_jwt_token(data.refresh_token)

    user_id, exp = (
        decoded_data["user_id"],
        datetime.fromtimestamp(decoded_data["exp"], tz=timezone.utc),
    )

    if exp < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=401, detail="Refresh token expired.Please log in"
        )
    access_token = generate_jwt_tokens(user_id, True)

    return {"access_token": access_token}


@router.get("/me", response_model=UserProfileResponse)
async def profil(current_user: current_user_jwt_dep):
    return current_user


@router.get("/log out")
async def log_out(session: db_deb, current_user: current_user_jwt_dep):
    current_user = None
    return "user log out"


@router.put("/update", response_model=UserProfileResponse)
async def update_profil(
    session: db_deb,
    update_data: UserProfilUpdateRequest,
    current_user: current_user_jwt_dep,
):
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(current_user, key, value)
    session.commit()
    session.refresh(current_user)
    return current_user
