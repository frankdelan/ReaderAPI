from sqlalchemy import select
from api.repositories.base import BaseRepository
from api.users.models import User
from database import async_session_factory


class UserRepository(BaseRepository):
    model = User

    async def get_password(self, user_id: int):
        async with async_session_factory() as session:
            query = select(self.model.password).where(self.model.user_id == user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
