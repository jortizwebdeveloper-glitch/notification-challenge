from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.user import UserModel

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class SendModel(Base):
    __tablename__ = "sends"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", name="send_user_fk_constraint"), index=True
    )
    job_id: Mapped[str] = mapped_column(Text)
    to: Mapped[str] = mapped_column(Text)
    title: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text)
    channel: Mapped[str] = mapped_column(String(20))
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    status: Mapped[str] = mapped_column(Text)
    log: Mapped[str] = mapped_column(Text, nullable=True)
    user: Mapped["UserModel"] = relationship(back_populates="sends")  # noqa: UP037

