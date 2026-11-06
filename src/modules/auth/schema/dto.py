from pydantic import BaseModel, Field

from src.shared.validate_fields import EmailField, PasswordField


class SigninRequest(BaseModel):
    username: EmailField = Field(
        description="Correo electrónico del usuario",
        examples=["usuario@correo.com"],
    )
    password: str = Field(
        description="Contraseña del usuario registrado",
        examples=["Secreta123!"],
    )


class SignupRequest(BaseModel):
    email: EmailField = Field(
        description="Correo electrónico del usuario. Debe ser único.",
        examples=["usuario@correo.com"],
    )
    password: PasswordField = Field(
        description="La contraseña debe contar con: Mínimo 8 caracteres de longitud, una letra minúscula, una letra mayúscula, un número, un carácter especial (símbolo)",
        examples=["Secreta123!"],
    )
