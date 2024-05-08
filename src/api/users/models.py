from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)

    book: Mapped[list["Book"]] = relationship(back_populates="user", lazy='selectin')