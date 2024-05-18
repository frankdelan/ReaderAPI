import pytest
from httpx import AsyncClient
from sqlalchemy import text

from api.books.queries import insert_book
from main import app
from api.books.models import *
from api.users.models import *
from database import async_engine, async_session_factory

USER_ID: int = 1


@pytest.fixture(scope='session', autouse=True)
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
