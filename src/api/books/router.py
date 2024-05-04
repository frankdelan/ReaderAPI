from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.books.queries import get_books_from_db, get_book_from_db
from database import get_async_session
from api.books.schemas import BookSchema

router = APIRouter(
    prefix='/book',
    tags=['books']
)


@router.get('/list', response_model=dict[str, str | list[BookSchema] | None])
async def get_books(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        books = await get_books_from_db(session, user_id)
    except Exception as e:
        return {'status': 'error',
                'data': None,
                'detail': str(e)}
    return {'status': 'success',
            'data': books,
            'detail': None}


@router.get('/{book_id}', response_model=dict[str, str | BookSchema | None])
async def get_book_by_id(book_id: int, user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        book = await get_book_from_db(session, book_id, user_id)
    except Exception as e:
        return {'status': 'error',
                'data': None,
                'detail': str(e)}
    return {'status': 'success',
            'data': book,
            'detail': None}
