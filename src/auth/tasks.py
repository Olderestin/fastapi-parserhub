from typing import List
from fastapi_mail import FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from starlette.responses import JSONResponse
import aiohttp

from config import conf
from auth.schemas import UserRead

async def send_verification_email(token: str, email: List[EmailStr]) -> JSONResponse:

    html = f"""Please click on the link below to confirm your registration:
    http://127.0.0.1:8000/auth/verify?token={token}"""

    message = MessageSchema(
        subject="Verification email",
        recipients=[email],
        body=html,
        subtype=MessageType.html)
    
    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})

async def send_verify_request(user: UserRead):
    url = "http://127.0.0.1:8000/auth/request-verify-token"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {"email": f"{user.email}"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data):
            pass

