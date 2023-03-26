from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer,
    String,
    Column,
    DateTime,
    ForeignKeyConstraint
)

Base = declarative_base()


class Books(Base):
    __tablename__ = "books"
    book_id = Column(Integer(), primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    published = Column(DateTime(timezone=True), default=datetime.now())
    date_added = Column(DateTime(timezone=True), default=datetime.now())
    date_deleted = Column(DateTime(timezone=True), nullable=True)


class Borrow(Base):
    __tablename__ = "borrow"
    borrow_id = Column(Integer(), primary_key=True)
    book_id = Column(Integer(), nullable=False)
    date_start = Column(DateTime(timezone=True), default=datetime.now())
    date_end = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer)
    __table_args__ = (
        ForeignKeyConstraint(['book_id'], ["books.book_id"], ondelete="CASCADE"),
    )

# sqlalchemy.url = postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
# from bot.database.models import Base
# target_metadata = Base.metadata
