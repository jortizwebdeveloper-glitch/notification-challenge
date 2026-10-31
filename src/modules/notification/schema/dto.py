from enum import StrEnum
from typing import Annotated, Any, TypedDict

from pydantic import BaseModel, BeforeValidator, Field
from pydantic_core import PydanticCustomError


class Channel(StrEnum):
    EMAIL = "email"
    SMS = ("sms",)
    PUSH_NOTIFICATION = "push_notification"


def _validate_channel(value: Any):
    try:
        return Channel(value)
    except ValueError:
        raise PydanticCustomError(
            "invalid_channel", "Canal invalido", {"channle": value}
        )


TitleField = Annotated[
    str, Field(max_length=50, min_length=5, examples=["Bienvenido a la plataforma"])
]
ContentlField = Annotated[
    str, Field(examples=["Gracias por registrarte. Completa tu perfil para empezar."])
]
ChannelField = Annotated[Channel, BeforeValidator(_validate_channel)]


class CreateNotificationRequest(BaseModel):
    title: TitleField
    content: ContentlField
    channel: ChannelField


class UpdateNotificationRequest(BaseModel):
    title: TitleField | None = None
    content: ContentlField | None = None
    channel: ChannelField | None = None


class NotificationData(TypedDict, total=False):
    title: str
    content: str
    channle: Channel
