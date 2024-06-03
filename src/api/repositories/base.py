from abc import ABC, abstractmethod

from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session_factory


class AbstractRepository(ABC):
    @abstractmethod
    async def get(self, pk):
        raise NotImplementedError()

    @abstractmethod
    async def create(self, data: dict):
        raise NotImplementedError()

    @abstractmethod
    async def update(self, pk, data: dict):
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, pk):
        raise NotImplementedError()


class BaseRepository(AbstractRepository):
    model = None

    async def get(self, pk: int):
        async with async_session_factory() as session:
            obj = await session.get(self.model, pk)
            return obj

    async def create(self, data: dict):
        async with async_session_factory() as session:
            obj = self.model(**data)
            session.add(obj)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise ValueError('Object already exists')
            await session.refresh(obj)
            return obj

    async def update(self, data: dict, filters):
        async with async_session_factory() as session:
            query = update(self.model).where(**filters).values(data).returning(self.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    async def delete(self, obj):
        async with async_session_factory() as session:
            await session.delete(obj)
            await session.commit()
            return obj.id
