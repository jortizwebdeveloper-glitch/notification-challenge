from typing import Annotated, TypedDict

from pydantic import BaseModel, Field

from src.shared.channels import Channel, ChannelField

TitleField = Annotated[
    str, Field(max_length=50, min_length=5, examples=["Bienvenido a la plataforma"])
]
ContentlField = Annotated[
    str, Field(examples=["Gracias por registrarte. Completa tu perfil para empezar."])
]


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


class ResponseNotification(BaseModel):
    id: int
    title: str
    content: str
    channel: str


class ResponseCreateNotification(BaseModel):
    notification: ResponseNotification
    jobs_ids: list[str] | None = None
