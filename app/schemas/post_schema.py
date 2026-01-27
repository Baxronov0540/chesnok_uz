from datetime import datetime

from pydantic import BaseModel


class PostCreateRequest(BaseModel):
    title: str
    body: str
    category_id: int
    views_count: int = 0
    likes_count: int = 0
    comments_count: int = 0


class PostListResponse(BaseModel):
    id: int
    title: str
    slug: str
    body: str
    category_id: int
    views_count: int
    likes_count: int
    comments_count: int
    is_active: bool
    created_at: datetime
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 4,
                    "title": "O'zbekistonda havo harorati tushib ketdi",
                    "slug": "o'zbekistonda-havo-harorati-tushib-ketdi",
                    "body": "O'zbekistonda havo harorati kundan kunga tushib ketyapti buni sababi shimoldan sovuq havo oqimi kirib kelishi bo'lyapti",
                    "category_id": 23,
                    "views_count": 1234,
                    "likes_count": 200,
                    "comments_count": 100000,
                    "is_active": True,
                    "created_at": "2026-01-19-789.009T",
                }
            ]
        }
    }


class PostUpdateRequest(BaseModel):
    title: str
    body: str
    is_active: bool
