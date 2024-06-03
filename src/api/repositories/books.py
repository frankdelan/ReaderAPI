from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from api.books.models import Book
from api.repositories.base import BaseRepository
from database import async_session_factory


class BookRepository(BaseRepository):
    model = Book

    async def get_list(self, user_id: int):
        async with async_session_factory() as session:
            query = (select(self.model).where(self.model.user_id == user_id))
            result = await session.execute(query)
            data = result.scalars().all()
            if not data:
                raise NoResultFound('Objects not found')
            return data

    async def get(self, user_id: int, book_id: int):
        async with async_session_factory() as session:
            query = (select(self.model).where((self.model.id == book_id) & (self.model.user_id == user_id)))
            result = await session.execute(query)
            data = result.scalar_one_or_none()
            if not data:
                raise NoResultFound('Object not found')
            return data
