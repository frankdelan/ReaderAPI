import pytest
from sqlalchemy import select

from api.books.models import Book
from api.books.queries import insert_book, get_book_from_db
from api.books.schemas import BookAdd, BookSchema
from database import async_session_factory


