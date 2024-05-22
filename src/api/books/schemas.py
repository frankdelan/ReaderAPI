from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict
from enum import Enum


class BookStatus(str, Enum):
    is_finished: str = 'Прочитано'
    is_reading: str = 'Читает'

    def __str__(self) -> str:
        return self.value


class ProgressSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    current_pages: int
    start_reading_date: date


class BookAdd(BaseModel):
    title: str
    author: Optional[str]
    volume: int


class BookSchema(BookAdd):
    model_config = ConfigDict(from_attributes=True)

    progress: ProgressSchema
    status: BookStatus
    id: int
