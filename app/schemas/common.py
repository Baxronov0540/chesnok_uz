from pydantic import BaseModel


class ProffesionInline(BaseModel):
    id: int
    name: str
