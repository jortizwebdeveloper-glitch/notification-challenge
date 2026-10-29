from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.auth.infra.auth_model import AuthModel
    from src.modules.notification.infra.notification_model import NotificationModdel

from src.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    auth: Mapped["AuthModel"] = relationship(back_populates="user")
    notifications: Mapped["NotificationModdel"] = relationship(back_populates="user")
