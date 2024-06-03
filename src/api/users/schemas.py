from pydantic import BaseModel


class AuthUser(BaseModel):
    user_id: int
    password: str
