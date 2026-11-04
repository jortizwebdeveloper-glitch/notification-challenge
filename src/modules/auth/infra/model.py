from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.user import UserModel

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base


class AuthModel(Base):
    __tablename__ = "auth"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", name="auth_user_foreing_key_constraint"),
        unique=True,
        index=True,
    )
    password: Mapped[str] = mapped_column(Text)
    user: Mapped[UserModel] = relationship(back_populates="auth")
