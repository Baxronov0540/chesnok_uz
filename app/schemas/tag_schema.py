from pydantic import BaseModel


class TagCreateRequest(BaseModel):
    name: str


class TagListResponse(BaseModel):
    id: int
    name: str
    slug: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 2,
                    "name": "Basketabll sport turi",
                    "slug": "basketball-sport-turi",
                }
            ]
        }
    }


class TagUpdateRequest(BaseModel):
    name: str | None = None
