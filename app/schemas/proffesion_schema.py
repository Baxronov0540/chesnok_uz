from pydantic import BaseModel


class ProffesionCreateRequest(BaseModel):
    name: str


class ProffesionListResponse(BaseModel):
    id: int
    name: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 2,
                    "name": "Muxbir",
                }
            ]
        }
    }


class ProffesionUpdateRequest(BaseModel):
    name: str | None = None
