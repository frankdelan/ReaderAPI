import pytest
from fastapi.encoders import jsonable_encoder

from api.books.models import Book
from api.books.queries import insert_book, get_books_from_db, get_book_from_db
from api.books.schemas import BookAdd, BookSchema
from database import async_session_factory
from tests.conftest import USER_ID


class TestAPI:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("data, user_id", [
        (BookAdd(title="Test1", author="Tester1", volume=100), USER_ID)
    ])
    async def test_book_by_id(self, get_client, data, user_id):
        async with async_session_factory() as session:
            result: Book = await insert_book(session, data, user_id)
            book: BookSchema = BookSchema.from_orm(result)
        response = await get_client.get(f"/book/{book.id}")
        assert response.status_code == 200
        assert response.json() == {"status":"success","data":jsonable_encoder(book),"detail":None}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_id", [USER_ID])
    async def test_book_list(self, get_client, user_id):
        async with async_session_factory() as session:
            result: list[Book] = await get_books_from_db(session, user_id)
            books: list[BookSchema] = list(map(lambda x: BookSchema.from_orm(x), result))
        response = await get_client.get("/book/list")
        assert response.status_code == 200
        assert response.json() == {"status":"success","data":jsonable_encoder(books),"detail":None}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("data, user_id", [
        (BookAdd(title="Dubrovskiy", author="Pushkin", volume=300), USER_ID)
    ])
    async def test_add_book(self, get_client, data, user_id):
        response = await get_client.post(f"/book/add?tg_id={user_id}",
                                         json={"title": data.title,
                                               "author": data.author,
                                               "volume": data.volume})
        json_data = response.json()
        async with async_session_factory() as session:
            result: Book = await get_book_from_db(session, json_data['data']["id"], user_id)
            book: BookSchema = BookSchema.from_orm(result)
        assert response.status_code == 200
        assert json_data == {"status":"success","data":jsonable_encoder(book),"detail":None}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("book_id", [1, 2])
    async def test_delete_book(self, get_client, book_id):
        response = await get_client.delete(f"/book/delete/{book_id}")
        assert response.status_code == 200
