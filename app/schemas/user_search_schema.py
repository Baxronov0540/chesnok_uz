from pydantic import BaseModel

from datetime import datetime

class UserSearchCreateRequest(BaseModel):

    term:str
    count:int|None = 0
class UserSearchListResponse(BaseModel):

    id:int
    term:str
    count:int
        