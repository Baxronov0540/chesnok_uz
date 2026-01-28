from pydantic import BaseModel
from datetime import datetime

class CommentCreateRequest(BaseModel):
    user_id: int
    text: str
    post_id: int

class CommentListResponse(BaseModel):
    id: int
    user_id: int
    text: str
    post_id: int
    is_active:bool
    created_at:datetime
    updated_at:datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 2,
                    "user_id": 12,
                    "text": "juda zo'r post ekan menda yaxshi tassurot uyg'otdi!!",
                    "post_id": 23,
                    "is_active":True,
                    "created_at": "2026-01-28T11:58:17.354024+05:00",
                    "updated_at":"2026-01-28T11:58:17.354024+05:00"
                }
            ]
        }
    }


class CommentUpdateRequest(BaseModel):
    text: str | None = None
    post_id: int | None = None
    updated_at:datetime|None = datetime.now()
