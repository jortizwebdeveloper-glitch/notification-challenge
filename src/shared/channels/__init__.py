from abc import ABC, abstractmethod
from enum import StrEnum

import markdown
from pydantic import BaseModel, Field, field_validator

from ..validate_fields import EmailField, PhoneField


class Channel(StrEnum):
    EMAIL = "email"
    SMS = "sms"
    PUSH_NOTIFICATION = "push_notification"


class ChannelData(BaseModel):
    title: str
    content: str
    channel: Channel
    to: str


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


class BaseChannel(ABC):
    """Clase base de un canal"""

    @abstractmethod
    def send(self) -> str:
        pass

    @abstractmethod
    def validate(self, data: ChannelData):
        pass


class EmailChannel(BaseChannel):
    def __init__(self, row: ChannelData):
        self._row = row

    def send(self):
        payload = self.validate(self._row)
        return payload

    def validate(self, row):
        return EmailModel(title=row.title, content=row.content, to=row.to)


class SMSChannel(BaseChannel):
    def __init__(self, row: ChannelData):
        self._row = row

    def send(self):
        payload = self.validate(self._row)
        return payload

    def validate(self, row):
        return SMSModel(title=row.title, content=row.content, to=row.to)


class PushNotificationChannel(BaseChannel):
    def send(self):
        return "Send Push Notification"


channels = {Channel.EMAIL: EmailChannel, Channel.SMS: SMSChannel}


def get_channel(row: ChannelData):
    C = channels.get(row.channel)
    return C(row) if C else None


# email = {
#     "channel": "email",
#     "title": "Novedades de nuestro boletín",
#     "content": "# Bienvenido\n\nGracias por ser parte de nuestra comunidad.\n\n## Qué encontrarás\n\n- Noticias y actualizaciones\n- Consejos útiles\n- Recursos recomendados\n\n| Sección | Descripción |\n|---|---|\n| Novedades | Resumen de lo más reciente |\n| Guías | Contenido práctico paso a paso |\n\n[Conoce más](https://ejemplo.com)\n\nUn saludo cordial,\n\n**El equipo**",
# }


# print(markdown.markdown(email["content"]))
