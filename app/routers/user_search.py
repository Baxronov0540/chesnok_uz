from fastapi import APIRouter
from sqlalchemy import select
from app.schemas import UserSearchListResponse
from app.models import UserSearch
from app.database import db_deb


router = APIRouter(prefix="/user_search", tags=["UserSearch"])


@router.get("/interisting/", response_model=list[UserSearchListResponse])
async def most_keywords_user(session: db_deb):
    stmt = select(UserSearch).order_by(UserSearch.count.desc()).limit(5)
    res = session.execute(stmt).scalars().all()
    return res
