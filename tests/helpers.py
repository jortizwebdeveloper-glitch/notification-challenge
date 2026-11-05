from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.modules.auth import AuthModel
from src.modules.notification import NotificationModel
from src.modules.user import UserModel


def getUser(session: Session, email: str):
    user = session.scalars(
        select(UserModel).where(UserModel.email == email)
    ).one_or_none()
    return user


async def async_get_user(session: AsyncSession, email: str):
    user = (
        await session.scalars(select(UserModel).where(UserModel.email == email))
    ).one_or_none()
    return user


def addUser(session: Session, email: str):
    user = UserModel(email=email)
    session.add(user)
    session.flush()
    return user


async def async_add_user(session: AsyncSession, email: str):
    stmt = insert(UserModel).values(email=email).returning(UserModel)
    user = (await session.scalars(stmt)).one()
    await session.flush()
    return user


def addAuth(session: Session, password: str, user_id: int):
    auth = AuthModel(password=password, user_id=user_id)
    session.add(auth)
    session.flush()
    return auth


def addNotification(session: Session, item: dict):
    stmt = insert(NotificationModel).values(item).returning(NotificationModel)
    notification = session.scalars(stmt).one()
    session.flush()
    return notification


async def async_add_notification(session: AsyncSession, item: dict):
    stmt = insert(NotificationModel).values(item).returning(NotificationModel)
    notification = (await session.scalars(stmt)).one()
    await session.flush()
    return notification
