from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.auth import AuthModel
    from src.modules.notification import NotificationModel

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    auth: Mapped[AuthModel] = relationship(back_populates="user")
    notifications: Mapped[list[NotificationModel]] = relationship(
        back_populates="user"
    )
