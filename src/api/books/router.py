from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.books.models import Book
from api.books.queries import get_books_from_db, get_book_from_db, insert_book, update_book_progress, \
    delete_book_from_db
from database import get_async_session
from api.books.schemas import BookSchema, BookAdd


router = APIRouter(
    prefix='/book',
    tags=['books']
)


@router.get('/list', response_model=dict[str, str | list[BookSchema] | None])
async def get_books(user_id: int,
                    session: AsyncSession = Depends(get_async_session)):
    try:
        books: list[Optional[Book]] = await get_books_from_db(session, user_id)
        return {'status': 'success',
                'data': books,
                'detail': None}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get('/{book_id}', response_model=dict[str, str | BookSchema | None])
async def get_book_by_id(book_id: int, user_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    try:
        book: Optional[Book] = await get_book_from_db(session, book_id, user_id)
        return {'status': 'success',
                'data': book,
                'detail': None}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post('/add', response_model=dict[str, str | BookSchema | None])
async def add_book(book: BookAdd, user_id: int,
                   session: AsyncSession = Depends(get_async_session)):
    try:
        book_data: Optional[Book] = await insert_book(session, book, user_id)
        return {'status': 'success',
                'data': book_data,
                'detail': None}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch('/progress/{book_id}', response_model=dict[str, str | BookSchema | None])
async def change_book_progress(book_id: int, user_id: int, current_page: int,
                               session: AsyncSession = Depends(get_async_session)):
    try:
        book: Optional[Book] = await update_book_progress(session, book_id, user_id, current_page)
        if book:
            return {'status': 'success',
                    'data': book,
                    'detail': 'Книга изменена'}
        else:
            return {'status': 'error',
                    'data': None,
                    'detail': 'Книга не найлена'}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/delete/{book_id}')
async def delete_book(user_id: int, book_id: int,
                      session: AsyncSession = Depends(get_async_session)):
    try:
        await delete_book_from_db(session, book_id, user_id)
        return {'status': 'success',
                'data': None,
                'detail': 'Книга была удалена'}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
