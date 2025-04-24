from fastapi import APIRouter

from .routers import auth_router, user_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
