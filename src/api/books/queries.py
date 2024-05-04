from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.books.models import Book, Progress


async def get_books_from_db(session: AsyncSession, user_id: int):
    query = (select(Book.id, Book.title, Book.author, Book.volume, Book.status,
                    Progress.current_pages, Progress.start_reading_date)
             .join(Progress, Book.id == Progress.book_id)
             .where(Book.user_id == user_id))
    result = await session.execute(query)
    data = result.mappings().all()
    return data


async def get_book_from_db(session: AsyncSession, book_id: int, tg_id: int):
    query = (select(Book.id, Book.title, Book.author, Book.volume, Book.status,
                    Progress.current_pages, Progress.start_reading_date)
             .join(Progress, Book.id == Progress.book_id)
             .where(Book.id == book_id and Book.user_id == tg_id))
    result = await session.execute(query)
    data = result.mappings().one()
    return data
