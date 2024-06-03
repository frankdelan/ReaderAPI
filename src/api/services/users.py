from typing import Type

from fastapi import Depends

from api.repositories.users import UserRepository
from api.users.schemas import AuthUser


class UserService:
    def __init__(self, repository: UserRepository = Depends(UserRepository)):
        self.repository: UserRepository = repository

    async def add_user(self, data: AuthUser):
        return await self.repository.create(data.model_dump())

    async def get_user_password(self, user_id: int) -> str:
        return await self.repository.get_password(user_id)
