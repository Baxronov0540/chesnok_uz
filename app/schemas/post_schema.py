from datetime import datetime

from pydantic import BaseModel

class PostCreateRequest(BaseModel):
    
    title:str
    body:str
    category_id:int
    views_count:int|None =0
    likes_count:int|None =0
    comments_count:int|None=0


class PostListResponse(BaseModel):
    
    id:int
    title:str
    slug:str
    body:str
    category_id:int
    views_count:int
    likes_count:int
    comments_count:int
    is_active:bool
    created_at:datetime

class PostUpdateRequest(BaseModel):
    
    title:str 
    body:str 
    is_active:bool  

