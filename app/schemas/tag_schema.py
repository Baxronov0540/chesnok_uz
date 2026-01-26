
from pydantic import BaseModel



class TagCreateRequest(BaseModel):
    name:str

class TagListResponse(BaseModel):
    id:int
    name:str
    slug:str

class TagUpdateRequest(BaseModel):
    name:str|None =None 