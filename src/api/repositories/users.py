from sqlalchemy import select
from api.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    async def get(self, user_id):
        query = select(self.model.password).where(self.model.tg_id == user_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
