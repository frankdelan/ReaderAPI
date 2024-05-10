from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.users.models import User
from database import Base


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    author: Mapped[Optional[str]]
    volume: Mapped[int]
    status: Mapped[str] = mapped_column(default='Читает')

    user_id: Mapped[int] = mapped_column(ForeignKey('user.tg_id'))
    user: Mapped[User] = relationship(User)

    progress: Mapped["Progress"] = relationship(back_populates="book", lazy='selectin')


class Progress(Base):
    __tablename__ = 'progress'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    book_id: Mapped[int] = mapped_column(ForeignKey('book.id', ondelete="CASCADE"))
    book: Mapped[Book] = relationship(Book)

    current_pages: Mapped[int] = mapped_column(default=0)
    start_reading_date = mapped_column(Date, default=datetime.now().date())
