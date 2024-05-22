import pytest
from httpx import AsyncClient
from sqlalchemy import text

from api.books.queries import insert_book
from api.books.schemas import BookSchema, BookAdd
from main import app
from api.books.models import *
from api.users.models import *
from database import async_engine

USER_ID: int = 1


@pytest.fixture(scope='session')
async def setup_database():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(f"INSERT INTO public.user VALUES ({USER_ID}, 'TestUser');"))
    yield


@pytest.fixture
async def get_client():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        yield client


@pytest.fixture
async def add_test_data():
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        response = await client.post(f"/book/add?user_id={USER_ID}",
                                     json={"title": "Test Book",
                                           "author": "Fake Author",
                                           "volume": 100})
        yield response.json()

        await client.delete(f"/book/delete/{response.json()['data']['id']}?user_id={USER_ID}")
