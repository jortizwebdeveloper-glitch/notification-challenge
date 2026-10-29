import re
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError


class SigninRequest(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_email(cls, value: str) -> str:
        pattern = r"^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,7}$"

        if not re.fullmatch(pattern, value):
            raise PydanticCustomError(
                "invalid_email_format",
                "Formato de email invalido",
                {"email": value},
            )

        return value

    password: str


class CustomError(Exception):
    """Custom Error"""


class SignupRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        pattern = r"^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,7}$"

        if not re.fullmatch(pattern, value):
            raise PydanticCustomError(
                "invalid_email_format",
                "Formato de email invalido",
                {"email": value},
            )

        return value

    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )

        if not re.fullmatch(pattern, value):
            raise PydanticCustomError(
                "invalid_password_format",
                "La contraseña debe contar con: Mínimo 8 caracteres de longitud. Al menos una letra minúscula. Al menos una letra mayúscula. Al menos un número. Al menos un carácter especial (símbolo)",
                {"password": value},
            )

        return value
