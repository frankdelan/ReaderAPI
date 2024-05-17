from datetime import date
from typing import Optional

from pydantic import BaseModel
from enum import Enum


class BookStatus(str, Enum):
    is_finished: str = 'Прочитано'
    is_reading: str = 'Читает'

    def __str__(self) -> str:
        return self.value


class ProgressSchema(BaseModel):
    current_pages: int
    start_reading_date: date

    class Config:
        from_attributes = True


class BookAdd(BaseModel):
    title: str
    author: Optional[str]
    volume: int


class BookSchema(BookAdd):
    progress: ProgressSchema
    status: BookStatus
    id: int

    class Config:
        from_attributes = True
