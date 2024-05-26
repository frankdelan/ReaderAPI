from sqlalchemy.ext.asyncio import AsyncSession

from api.users.models import User
from api.repositories.users import UserRepository


class UserService:
    @staticmethod
    async def add_user(session: AsyncSession, user_id: int, password: str) -> User:
        user: User = User(tg_id=user_id, password=password)
        repository = UserRepository(session, User)
        return await repository.add(user)

    @staticmethod
    async def get_password(session: AsyncSession, user_id: int) -> str:
        repository = UserRepository(session, User)
        return await repository.get(user_id)
