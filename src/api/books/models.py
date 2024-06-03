from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.users.models import User
from database import Base


class Book(Base):
    __tablename__ = 'book'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    author: Mapped[Optional[str]]
    volume: Mapped[int]
    status: Mapped[str] = mapped_column(default='Читает')

    user_id: Mapped[int] = mapped_column(ForeignKey('user.user_id'))
    user: Mapped["User"] = relationship(back_populates="book")

    progress: Mapped["Progress"] = relationship(back_populates="book", lazy='selectin', cascade="all, delete-orphan")


class Progress(Base):
    __tablename__ = 'progress'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    book_id: Mapped[int] = mapped_column(ForeignKey('book.id'))
    book: Mapped["Book"] = relationship(back_populates="progress")

    current_pages: Mapped[int] = mapped_column(default=0)
    start_reading_date = mapped_column(Date, default=datetime.now().date())
