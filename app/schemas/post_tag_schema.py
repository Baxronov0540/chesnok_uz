from pydantic import BaseModel

class PostTagCreateRequest(BaseModel):
    post_id:int
    tag_id:int

class PostTagListResponse(BaseModel):
    post_id:int
    tag_id:int

class PostTagUpdateRequest(BaseModel):
    post_id:int|None = None
    tag_id:int|None = None




