from fastapi import APIRouter

from .basic import router as basic_router
from .register import router as register_router
from .session import router as session_router

app = APIRouter()

app.include_router(basic_router)
app.include_router(register_router)
app.include_router(session_router)
