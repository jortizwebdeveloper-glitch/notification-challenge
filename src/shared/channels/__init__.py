import asyncio
from abc import ABC, abstractmethod

import markdown
from pydantic import BaseModel, Field, field_validator

from ..validate_fields import (
    Channel,
    ChannelField,
    EmailField,
    PhoneField,
    TokenFcmField,
)


class ChannelData(BaseModel):
    title: str | None = None
    content: str | None = None
    channel: ChannelField | None = None
    to: str | None = None


class EmailModel(BaseModel):
    title: str
    content: str
    to: EmailField | None = None

    @field_validator("content", mode="after")
    @classmethod
    def _md_to_HTML(cls, value: str) -> str:
        return markdown.markdown(value)


class SMSModel(BaseModel):
    title: str
    content: str = Field(max_length=160)
    to: PhoneField | None = None


class PushModel(BaseModel):
    title: str
    content: str = Field(max_length=160)
    to: TokenFcmField | None = None


class BaseChannel(ABC):
    """Clase base de un canal"""

    def __init__(self, row: ChannelData):
        self._row = row

    @property
    def src(self) -> str:
        pass

    async def send(self):
        payload = await asyncio.to_thread(self.validate, self._row)
        return payload

    @abstractmethod
    def validate(self, data: ChannelData):
        pass

    def open_src(self):
        with open(self.src, "r", encoding="utf8") as src:
            return src.read().splitlines()


class EmailChannel(BaseChannel):
    src = "src/core/txt/email.txt"

    def validate(self, row):
        return EmailModel(title=row.title, content=row.content, to=row.to)


class SMSChannel(BaseChannel):
    src = "src/core/txt/sms.txt"

    def validate(self, row):
        return SMSModel(title=row.title, content=row.content, to=row.to)


class PushNotificationChannel(BaseChannel):
    src = "src/core/txt/push.txt"

    def validate(self, row):
        return PushModel(title=row.title, content=row.content, to=row.to)


channels = {Channel.EMAIL: EmailChannel, Channel.SMS: SMSChannel, Channel.PUSH_NOTIFICATION: PushNotificationChannel}


def get_channel(row: ChannelData) -> BaseChannel:
    C = channels.get(row.channel)
    return C(row) if C else None
