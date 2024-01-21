from fastapi import APIRouter, Depends, status, Request, Body, HTTPException, Query
from fastapi_users import exceptions, models, schemas
from pydantic import EmailStr
from fastapi_users.manager import BaseUserManager
from fastapi_users.router.common import ErrorCode, ErrorModel

from auth.schemas import UserCreate, UserRead
from auth.base_config import auth_backend, fastapi_users, current_user, get_user_manager
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

@router.post(
    "/auth/request-verify-token",
    status_code=status.HTTP_202_ACCEPTED,
    name="verify:request-token",
    tags=["auth"],
)
async def request_verify_token(
    request: Request,
    email: EmailStr = Body(..., embed=True),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    try:
        user = await user_manager.get_by_email(email)
        await user_manager.request_verify(user, request)
    except (
        exceptions.UserNotExists,
        exceptions.UserInactive,
        exceptions.UserAlreadyVerified,
    ):
        pass

    return None

@router.get(
    "/auth/verify",
    response_model=UserRead,
    name="verify:verify",
    tags=["auth"],
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.VERIFY_USER_BAD_TOKEN: {
                            "summary": "Bad token, not existing user or"
                            "not the e-mail currently set for the user.",
                            "value": {"detail": ErrorCode.VERIFY_USER_BAD_TOKEN},
                        },
                        ErrorCode.VERIFY_USER_ALREADY_VERIFIED: {
                            "summary": "The user is already verified.",
                            "value": {
                                "detail": ErrorCode.VERIFY_USER_ALREADY_VERIFIED
                            },
                        },
                    }
                }
            },
        }
    },
)
async def verify(
    request: Request,
    token: str = Query(..., embed=True),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    try:
        user = await user_manager.verify(token, request)
        return schemas.model_validate(UserRead, user)
    except (exceptions.InvalidVerifyToken, exceptions.UserNotExists):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.VERIFY_USER_BAD_TOKEN,
        )
    except exceptions.UserAlreadyVerified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.VERIFY_USER_ALREADY_VERIFIED,
        )