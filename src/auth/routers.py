from fastapi import APIRouter
from auth.schemas import UserCreate, UserRead

from auth.base_config import auth_backend
from auth.base_config import fastapi_users
router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)