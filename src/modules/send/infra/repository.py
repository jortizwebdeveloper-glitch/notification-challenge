from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, defer

from ..infra.model import SendModel
from ..schema.dto import SendData
from ..schema.ports import SendRepositoryPort


class SendRepository(SendRepositoryPort):
    def __init__(self, async_session: AsyncSession, session: Session):
        self._async_session = async_session
        self._session = session

    def find_all_by_user_id(self, user_id: int):
        stmt = (
            select(SendModel)
            .options(defer(SendModel.user_id))
            .where(SendModel.user_id == user_id)
        )
        rows = self._session.scalars(stmt).all()
        return rows

    async def async_create(self, body: SendData, user_id: int):
        stmt = (
            insert(SendModel)
            .options(defer(SendModel.user_id))
            .values(**body, user_id=user_id)
            .returning(SendModel)
        )
        row = (await self._async_session.scalars(stmt)).one()
        await self._async_session.commit()
        await self._async_session.refresh(row)

        return row
