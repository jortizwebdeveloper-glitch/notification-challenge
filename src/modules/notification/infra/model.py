from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.user import UserModel

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)
    channel: Mapped[str] = mapped_column(String(20))
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", name="notification_user_foreign_key_constraint"),
        index=True,
    )
    user: Mapped["UserModel"] = relationship(back_populates="notifications")  # noqa: UP037
