import re
from typing import Annotated

from pydantic import BeforeValidator
from pydantic_core import PydanticCustomError


def _validate_phone(value: str):
    pattern = r"^(?:\+57|57|0057)?3\d{9}$"
    if not re.fullmatch(pattern, value):
        raise PydanticCustomError(
            "invalid_phone_format", "Formato de celular invalido", {"phone": value}
        )
    return value


PhoneField = Annotated[str, BeforeValidator(_validate_phone)]


def _validate_email(value: str) -> str:
    pattern = (
        r"^[a-zA-Z0-9_+&*-]+(?:\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,7}$"
    )

    if not re.fullmatch(pattern, value):
        raise PydanticCustomError(
            "invalid_email_format",
            "Formato de email invalido",
            {"email": value},
        )

    return value


EmailField = Annotated[str, BeforeValidator(_validate_email)]


def _validate_password(value: str) -> str:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

    if not re.fullmatch(pattern, value):
        raise PydanticCustomError(
            "invalid_password_format",
            "La contraseña debe contar con: Mínimo 8 caracteres de longitud. Al menos una letra minúscula. Al menos una letra mayúscula. Al menos un número. Al menos un carácter especial (símbolo)",
            {"password": value},
        )

    return value


PasswordField = Annotated[str, BeforeValidator(_validate_password)]
