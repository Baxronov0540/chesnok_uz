from pydantic import BaseModel
from datetime import datetime


class UserCreateRequest(BaseModel):
    proffesion_id: int
    email: str
    avatar_id: int | None = None
    password_hash: str
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    post_count: int | None = 0
    post_read_count: int | None = 0
    is_active: bool | None = True
    is_staff: bool | None = False
    is_supperuser: bool | None = False


class UserListResponse(BaseModel):
    id: int
    proffesion_id: int
    email: str
    avatar_id: int | None
    password_hash: str
    first_name: str | None
    last_name: str
    bio: str | None = None
    post_count: int
    post_read_count: int
    is_active: bool
    is_staff: bool
    is_supperuser: bool
    created_at: datetime
    updated_at: datetime
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 4,
                    "profession_id": 3,
                    "email": "baxronovasror00@gmail.com",
                    "avatar_id": 3,
                    "password": "asror@24",
                    "first_name": "Asror",
                    "last_name": "Baxronov",
                    "bio": "Men talabaman",
                    "is_active": True,
                    "created_at": "2026-01-19-789.009T",
                }
            ]
        }
    }


class UserUpdateRequest(BaseModel):
    proffesion_id: int | None = None
    email: str | None = None
    avatar_id: int | None = None
    password_hash: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    post_count: int | None = None
    post_read_count: int | None = None
    is_active: bool | None = None
    is_staff: bool | None = None
    is_supperuser: bool | None = None


class CookieData(BaseModel):
    key: str
    value: str


class CokieTheme(BaseModel):
    pass
