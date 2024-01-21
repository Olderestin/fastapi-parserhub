from dotenv import load_dotenv
import os

from fastapi_mail import ConnectionConfig

load_dotenv()

DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")

SECRET_AUTH = os.environ.get("SECRET_AUTH")

conf = ConnectionConfig(
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME"),
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD"),
    MAIL_FROM = os.environ.get("MAIL_FROM"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="ParserHub",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = False
)