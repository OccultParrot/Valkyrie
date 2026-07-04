from fastapi import APIRouter
from .users import router as u_router
from .commands import router as c_router

router = APIRouter()

router.include_router(u_router)
router.include_router(c_router)
