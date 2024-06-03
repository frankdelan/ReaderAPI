from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from api.books.models import Book, Progress
from api.books.schemas import BookAdd
from api.repositories.books import BookRepository


class BookService:
    @staticmethod
    async def get_book_list(session: AsyncSession, user_id: int):
        repository = BookRepository(session)
        return await repository.get_list(user_id)

    @staticmethod
    async def get_book(session: AsyncSession, user_id: int, book_id: int):
        repository = BookRepository(session)
        return await repository.get(user_id, book_id)

    @staticmethod
    async def add_book(session: AsyncSession, data: BookAdd, user_id: int):
        book = Book(**data.model_dump(), user_id=user_id,
                    progress=Progress(current_pages=0, start_reading_date=datetime.now().date()))
        repository = BookRepository(session)
        return await repository.create(book)

    @staticmethod
    async def update_book(session: AsyncSession, user_id: int, book_id: int, page: int):
        repository = BookRepository(session)
        book = await repository.get(user_id, book_id)
        if book:
            if book.volume > page:
                book.progress.current_pages = page
            else:
                book.progress.current_pages = book.volume
                book.status = 'Прочитано'
        return await repository.update(book)

    @staticmethod
    async def delete_book(session: AsyncSession, user_id: int, book_id: int):
        repository = BookRepository(session)
        obj = repository.get(user_id, book_id)
        return await repository.delete(obj)
