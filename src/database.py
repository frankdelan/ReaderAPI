from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from config import DB_NAME, DB_HOST, DB_PORT, DB_PASS, DB_USER

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

Base = declarative_base()

async_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
