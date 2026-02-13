from .admin import router as admin_router
from .admin_boshqaruv import router as admin_boshqaruv_router

from fastapi import APIRouter

app = APIRouter()
app.include_router(admin_router)
app.include_router(admin_boshqaruv_router)

