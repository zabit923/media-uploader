from fastapi import APIRouter

from api.records.router import router as records_router
from api.users.router import router as users_router

router = APIRouter(prefix="")
router.include_router(users_router, tags=["users"])
router.include_router(records_router, tags=["records"])
