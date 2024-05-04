from pydantic import BaseModel


class RegisterUser(BaseModel):
    tg_id: int
    username: str


