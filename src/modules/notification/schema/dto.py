from enum import StrEnum

from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError


class Channel(StrEnum):
    EMAIL = "email"
    SMS = ("sms",)
    PUSH_NOTIFICATION = "push_notification"


class CreateNotificationRequest(BaseModel):
    title: str = Field(max_length=50, examples=["Bienvenido a la plataforma"])
    content: str = Field(
        examples=["Gracias por registrarte. Completa tu perfil para empezar."]
    )
    channel: Channel

    @field_validator("channel", mode="before")
    @classmethod
    def validate_channel(cls, value: str) -> str:
        try:
            return Channel(value)
        except ValueError:
            raise PydanticCustomError(
                "invalid_channel", "Canal invalido", {"channle": value}
            )
