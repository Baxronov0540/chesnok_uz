from pydantic import BaseModel



class UserSearchCreateRequest(BaseModel):
    term: str
    count: int | None = 0


class UserSearchListResponse(BaseModel):
    id: int
    term: str
    count: int
