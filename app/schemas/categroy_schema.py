from pydantic import BaseModel


class CategoryCreateRequest(BaseModel):
    name: str


class CategoryListResponse(BaseModel):
    id: int
    name: str
    slug: str
    model_config = {
        "json_schema_extra": {
            "examples": [{"id": 2, "name": "Jahon xabrlari", "slug": "jahon-xabarlari"}]
        }
    }


class CategoryUpdateRequest(BaseModel):
    name: str | None = None
