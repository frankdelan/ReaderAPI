from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.books.models import Book, Progress
from api.books.schemas import BookAdd
from api.books.utils import convert_data


async def get_books_from_db(session: AsyncSession,
                            user_id: int) -> list[Book]:
    query = (select(Book.id, Book.title, Book.author, Book.volume, Book.status,
                    Progress.current_pages, Progress.start_reading_date)
             .join(Progress, Book.id == Progress.book_id)
             .where(Book.user_id == user_id))
    result = await session.execute(query)
    data = result.mappings().all()
    books = [convert_data(item) for item in data]
    return books


async def get_book_from_db(session: AsyncSession,
                           book_id: int, tg_id: int) -> Book:
    query = (select(Book.id, Book.title, Book.author, Book.volume, Book.status,
                    Progress.current_pages, Progress.start_reading_date)
             .join(Progress)
             .where((Book.id == book_id) & (Book.user_id == tg_id)))
    result = await session.execute(query)
    data = result.mappings().one()
    book = convert_data(data)
    return book


async def insert_book(session: AsyncSession,
                      data: BookAdd, user_id: int) -> Book | None:
    book = Book(**data.dict(), status='Читает', user_id=user_id)
    progress = Progress(book=book, current_pages=0, start_reading_date=datetime.now().date())
    book.progress = progress
    try:
        session.add(book)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise 'Книга уже существует'
    else:
        return book


async def update_book_progress(session: AsyncSession,
                               book_id: int, tg_id: int, page: int) -> Book | None:
    query = select(Book).where((Book.id == book_id) & (Book.user_id == tg_id))
    data = await session.execute(query)
    book = data.scalar()
    if book:
        if book.volume >= page:
            book.progress.current_pages = page
        else:
            book.progress.current_pages = book.volume
            book.status = 'Прочитано'
        await session.commit()
        await session.refresh(book)
        return book
    else:
        return None


async def delete_book_from_db(session: AsyncSession,
                              book_id: int, tg_id: int):
    query = select(Book).where((Book.id == book_id) & (Book.user_id == tg_id))
    data = await session.execute(query)
    book = data.scalar()
    session.delete(book)
    await session.commit()
