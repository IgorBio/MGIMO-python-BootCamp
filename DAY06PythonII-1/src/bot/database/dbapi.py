import asyncio
from datetime import date
from datetime import datetime
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.database.models import (
    Books,
    Borrow,
    Base
)

connection_string = f"postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
engine = create_async_engine(url=connection_string, echo=True, future=True, poolclass=NullPool)
sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


class DatabaseConnector:

    def str_to_datetime(self, date: str) -> datetime:
        return datetime.strptime(date + "/01/01", "%Y/%m/%d")

    async def add(self, session: AsyncSession, title: str, author: str, published: str):
        query = Books(
            title=title,
            author=author,
            published=self.str_to_datetime(published)
        )
        session.add(query)
        try:
            await session.commit()
            return {"book_id": query.book_id}
        except Exception as e:
            print(f"ERROR: {e}")
            return {"status_code": False}

    async def list_books(self, session):
        query = select(Books)
        result = await session.execute(query)
        m_list = [(book.title, book.author, book.published, book.date_deleted) for book in result.scalars()]
        return m_list

    async def select_for_delete(self, session: AsyncSession, title: str, author: str, published: str):
        query = select(Books).where(
            and_(Books.title == title, Books.author == author))
        result = await session.execute(query)
        m_list = [(book.title, book.author, book.published, book.book_id) for book in result.scalars()]
        return m_list

    async def delete(self, session: AsyncSession, title: str, author: str, published: str):
        print(title, author)
        query = select(Borrow).where(
            Borrow.book_id == (select(Books.book_id).where(Books.title == title))
        )
        result = await session.execute(query)
        m_list = []
        book_id_in_borrow = None
        for i in result.scalars():
            m_list.append(i.date_start)
            m_list.append(i.date_end)
            book_id_in_borrow = i.book_id
        if m_list:
            if m_list[-1] is not None and m_list[-1] < datetime.now():
                query = update(Books).where(Books.book_id == book_id_in_borrow).values(
                    date_deleted=datetime.now().strftime("%Y-%m-%d"))
                # await session.execute(delete(Books).where(Books.book_id == book_id_in_borrow))
                await session.execute(query)
                await session.commit()
                return "Книга удалена"
        return " Невозможно удалить книгу"

    async def find(self, session: AsyncSession, title: str, author: str, published: str):
        query = select(Books).where(and_(Books.title == title, Books.author == author))
        try:
            result = await session.execute(query)
            m_list = [(book.title, book.author, book.published) for book in result.scalars()]
            result = f"Найдена книга: {m_list[0][0]} {m_list[0][1]} {m_list[0][2]}"
        except:
            result = "Такой книги у нас нет"
        return result

    async def select_book_id_date_deleted(self, session: AsyncSession, title: str, author: str):
        query = select(Books).where(
            and_(Books.title == title, Books.author == author))
        result = await session.execute(query)
        m_list = []
        for book in result.scalars():
            if book.date_deleted is not None:
                m_list.append(book.book_id)
        return m_list

    async def borrow(self, session: AsyncSession, book_id: int, date_start: str, user_id: int):
        query = Borrow(
            book_id=book_id,
            date_start=datetime.strptime(date_start, "%Y-%m-%d"),
            # date_end=self.str_to_datetime(date_end),
            user_id=user_id
        )
        try:
            session.add(query)
            await session.commit()
            return "Вы взяли книгу."
        except Exception as e:
            print(e)
            return "Книгу сейчас невозможно взять."

    async def retrieve(self, session: AsyncSession, book_id: int, user_id: int) -> list:
        query = update(Borrow).where(and_(Borrow.book_id == book_id, Borrow.user_id == user_id)).values(
            date_end=datetime.now()
        )
        flag = 0
        try:
            await session.execute(query)
            await session.commit()
            flag = 1
        except:
            pass
        if flag:
            query_two = select(Books).where(Books.book_id == book_id)
            result = await session.execute(query_two)
        m_list = []
        for book in result.scalars():
            m_list.append(book.title)
            m_list.append(book.author)
            m_list.append(book.published)
        return m_list


async def main():
    testing = DatabaseConnector()
    # await testing.add("H", "M", "1995")
    # await testing.select_for_delete("S", "M", "1995")
    a = await testing.find('A', 'B', '2023')
    print(a)


if __name__ == "__main__":
    asyncio.run(main())
    # a = datetime.date(datetime.now())
    # b = date(2020, 7, 15)
    # print(type(a))
    # print(type(b))
    # print(a > b)
    # with suppress(IntegrityError):
    #     await session.commit()

# curl -X POST -H "Content-Type: application/json" -d '{"title": "linuxize", "author": "linuxize@example.com", "published": "2020-12-12"}' localhost:5000/add
