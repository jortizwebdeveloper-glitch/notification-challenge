from pydantic import BaseModel

from src.shared.validate_fields import EmailField, PasswordField


class SigninRequest(BaseModel):
    username: EmailField
    password: str


class CustomError(Exception):
    """Custom Error"""


class SignupRequest(BaseModel):
    email: EmailField
    password: PasswordField
