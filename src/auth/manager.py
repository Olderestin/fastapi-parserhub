import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from auth.models import User
from auth.utils import get_user_db
from config import SECRET_AUTH
from auth.tasks import send_verification_email
from auth.tasks import send_verify_request


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        await send_verify_request(user)


    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # print(f"Verification requested for user {user.id}. Verification token: {token}")
        await send_verification_email(token, user.email)

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)