from pydantic import BaseModel


class PostTagCreateRequest(BaseModel):
    post_id: int
    tag_id: int


class PostTagListResponse(BaseModel):
    post_id: int
    tag_id: int
    model_config = {"json_schema_extra": {"examples": [{"post_id": 2, "tag_id": 3}]}}


class PostTagUpdateRequest(BaseModel):
    post_id: int | None = None
    tag_id: int | None = None
