from typing import Optional

import pytest
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from api.books.models import Book
from api.books.queries import insert_book, get_books_from_db, get_book_from_db
from api.books.schemas import BookAdd, BookSchema
from database import async_session_factory
from tests.conftest import USER_ID


async def form_db_response(data: BookSchema, detail: Optional[str] = None):
    return {"status": "success",
            "data": jsonable_encoder(data),
            "detail": detail}


class TestSuccessAPI:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_id", [USER_ID])
    async def test_book_by_id(self, get_client, user_id, add_test_data):
        response = await get_client.get(f"/book/{add_test_data.id}?user_id={user_id}")
        assert response.status_code == 200
        assert response.json() == await form_db_response(add_test_data)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_id", [USER_ID])
    async def test_book_list(self, get_client, user_id):
        async with async_session_factory() as session:
            result: list[Book] = await get_books_from_db(session, user_id)
            books: list[BookSchema] = list(map(lambda x: BookSchema.model_validate(x), result))
        response = await get_client.get(f"/book/list?user_id={user_id}")
        assert response.status_code == 200
        assert response.json() == {"status":"success","data":jsonable_encoder(books),"detail":None}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("data, user_id", [
        (BookAdd(title="Dubrovskiy", author="Pushkin", volume=300), USER_ID)
    ])
    async def test_add_book(self, get_client, data, user_id):
        response = await get_client.post(f"/book/add?user_id={user_id}",
                                         json={"title": data.title,
                                               "author": data.author,
                                               "volume": data.volume})
        json_data = response.json()
        async with async_session_factory() as session:
            result: Book = await get_book_from_db(session, json_data['data']["id"], user_id)
            book: BookSchema = BookSchema.model_validate(result)
        assert response.status_code == 200
        assert json_data == await form_db_response(book)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("book_id, user_id, current_page", [
        (1, USER_ID, 100), (2, USER_ID, 200)
    ])
    async def test_change_progress(self, get_client, book_id, user_id, current_page):
        response = await get_client.patch(f"/book/progress/{book_id}?user_id={user_id}&current_page={current_page}")
        json_data = response.json()
        async with async_session_factory() as session:
            result: Book = await get_book_from_db(session, json_data['data']["id"], user_id)
            book: BookSchema = BookSchema.model_validate(result)
        assert response.status_code == 200
        assert json_data == await form_db_response(book, 'Книга изменена')

    @pytest.mark.asyncio
    @pytest.mark.parametrize("book_id, user_id", [(1, USER_ID), (2, USER_ID)])
    async def test_delete_book(self, get_client, book_id, user_id):
        response = await get_client.delete(f"/book/delete/{book_id}?user_id={user_id}")
        assert response.status_code == 200


class TestErrorAPI:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("book_id, user_id", [
        (1, 2), (10, 1), ('5', '5')
    ])
    async def test_book_by_id(self, get_client, book_id, user_id, add_test_data):
        response = await get_client.get(f"/book/{book_id}?user_id={user_id}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    @pytest.mark.parametrize("user_id", [
        5, '5'
    ])
    async def test_book_list(self, get_client, user_id):
        response = await get_client.get(f"/book/list?user_id={user_id}")
        assert response.status_code == 404
