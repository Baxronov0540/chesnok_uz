from fastapi import APIRouter
from fastapi.security import HTTPBasic

from app.database import db_deb
from app.schemas import (
    UserProfileResponse,
    current_user_basic_dep,
    UserProfilUpdateRequest,
)

basic = HTTPBasic()
router = APIRouter(prefix="/basic", tags=["Auth"])


@router.get("/profile", response_model=UserProfileResponse)
async def user_profile(db: db_deb, current_user: current_user_basic_dep):
    return current_user


@router.put("/profil/update/", response_model=UserProfileResponse)
async def profil_update(
    update_data: UserProfilUpdateRequest,
    db: db_deb,
    current_user: current_user_basic_dep,
):
    for attr, value in update_data.model_dump(exclude_unset=True).items():
        setattr(current_user, attr, value)
    db.commit()
    db.refresh(current_user)

    return current_user


@router.delete("/profil/deleted", status_code=204)
async def profil_deleted(db: db_deb, current_user: current_user_basic_dep):
    current_user.is_active = False
    current_user.is_deleted = True
    current_user.deleted_email = current_user.email
    current_user.email = None

    db.commit()
