from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.database import db_deb
from app.models import User,Post
from app.schemas import UserListResponse, UserCreateRequest,PostCreateRequest,PostListResponse
from app.utils import *
router = APIRouter(prefix="/user-auth", tags=["UserAuth"])

@router.get("/profile/",response_model=UserListResponse)
async def  user_profile(session:db_deb,email:str):

    stmt=select(User).where(User.email==email)
    res=session.execute(stmt).scalars().first()
    if not res:
        raise HTTPException(status_code=404,detail="User Not found")
    return res



# @router.post("/create", response_model=PostListResponse)
# async def post_create(session: db_deb, create_data: PostCreateRequest):
#     stmt=select(User).where(User.id==create_data.user_id)
#     res=session.execute(stmt).scalars().first()
#     res1=await user_profile(session=db_deb,email=res.email)
#     if res1.is_staff:
#         post = Post(
#             title=create_data.title,
#             body=create_data.body,
#             slug=generate_slug(create_data.title),
#             category_id=create_data.category_id,
#             user_id=create_data.user_id
#         )

#         session.add(post)
#         session.commit()
#         session.refresh(post)

#         return post
#     return HTTPException(status_code=400)







