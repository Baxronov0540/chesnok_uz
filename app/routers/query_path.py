from typing import Annotated
from fastapi import APIRouter, Path, HTTPException, status, Header, Query

router = APIRouter(prefix="auth", tags=["Auth"])


@router.get("/profile/{user_id}")
async def fet_profile(user_id: Annotated[int, Path]):
    pass


router.get("/admin/{admin_id}")


async def admin_access(
    admin_id: Annotated[int, Path(title="Admin ID", ge=1)],
    token: Annotated[str, Query(title="Admin maxfiy token")],
):
    if admin_id == 1 and token == "admin777":
        return {"admin": "Farrukh", "status": "Admin huquqi tasdiqlandi"}
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="sizda adminliok huquqi yuq (Path+Query xatosi)",
    )


@router.get("/secret_data")
async def get_search_data(
    x_token: Annotated[
        str | None, Header(description="Maxfiy token:my-secret-token")
    ] = None,
):
    if x_token == "admin123":
        return {
            "data": "Bu juda maxfiy ma'lumot, uni faqat Header orqali ko'rish mumkin!"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="not autohorized"
    )
