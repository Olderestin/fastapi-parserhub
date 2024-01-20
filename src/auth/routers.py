from fastapi import APIRouter, Depends
from fastapi_users import schemas

from auth.schemas import UserCreate, UserRead
from auth.base_config import auth_backend, fastapi_users, current_user
from auth.models import User

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

@router.get("/profile", tags=["auth"])
async def get_current_user(user: User = Depends(current_user)):
    return schemas.model_validate(UserRead, user)