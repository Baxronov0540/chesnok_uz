from pydantic import BaseModel

class CategoryCreateRequest(BaseModel):
    name:str

class CategoryListResponse(BaseModel):
    id:int
    name:str 
    slug:str 


class CategoryUpdateRequest(BaseModel):
    name:str|None =None    
