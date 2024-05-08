from datetime import date
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


class BookAdd(BaseModel):
    title: str
    author: str | None
    volume: int


class BookSchema(BookAdd):
    progress: ProgressSchema
    id: int
