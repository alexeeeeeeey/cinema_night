from fastapi import APIRouter

from .auth import router as auth_router
from .halls import router as halls_router
from .movies import router as movies_router
from .users import router as users_router

router = APIRouter(prefix="/v1")
router.include_router(users_router)
router.include_router(auth_router)
router.include_router(movies_router)
router.include_router(halls_router)
