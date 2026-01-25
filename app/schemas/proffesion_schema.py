from pydantic import BaseModel


class ProffesionCreateRequest(BaseModel):
    name:str

class ProffesionListResponse(BaseModel):
    id:int
    name:str

class ProffesionUpdateRequest(BaseModel):
    name:str|None =None
    