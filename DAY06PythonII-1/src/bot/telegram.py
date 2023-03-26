import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, BotCommand, BotCommandScopeDefault
from typing import Callable, Awaitable, Dict, Any

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from aiogram import Router, html
from aiogram.filters import CommandStart, Command

from pydantic import BaseSettings, SecretStr, PostgresDsn

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.dbapi import DatabaseConnector

from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from datetime import datetime

db = DatabaseConnector()


async def set_default_commands(bot):
    """Set of commands with description"""
    await bot.set_my_commands([
        BotCommand(command="start", description="Старт"),
        BotCommand(command="delete", description="Удаление одной книги"),
        BotCommand(command="list", description="Список книг"),
        BotCommand(command="find", description="Поиск книги"),
        BotCommand(command="borrow", description="Бронирование книги"),
        BotCommand(command="retrieve", description="Вернуть книгу"),
        BotCommand(command="stats", description="Статистика книги")
    ], scope=BotCommandScopeDefault())


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: PostgresDsn

    class Config:
        env_file = '../.env'
        env_file_encoding = 'utf-8'


config = Settings()


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)


router = Router(name="commands-router")


class Add(StatesGroup):
    title = State()
    author = State()
    published = State()


class Delete(StatesGroup):
    title_delete = State()
    author_delete = State()
    published_delete = State()
    user_answer = State()


class Find(StatesGroup):
    title_find = State()
    author_find = State()
    published_find = State()


class Borrow(StatesGroup):
    title_borrow = State()
    author_borrow = State()
    published_borrow = State()
    user_answer_borrow = State()


class Retrieve(StatesGroup):
    title_retrieve = State()
    author_retrieve = State()


add_router = Router()

list_router = Router()

delete_router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """
    Handles /start command
    :param message: Telegram message with "/start" text
    """
    await message.answer("""/add
/delete
/list
/find
/borrow
/retrieve
/stats
    """, reply_markup=ReplyKeyboardRemove()
                         )


@add_router.message(Command("add"))
async def cmd_add(message: Message, state: FSMContext) -> None:
    """
    Handles /play command
    :param message: Telegram message with "/add" text
    :param session: DB connection session
    """
    await state.set_state(Add.title)
    await message.answer("Введите название книги:")
    # await db.add(session=session)


@add_router.message(Add.title)
async def process_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(Add.author)
    await message.answer("Введите автора:")


@add_router.message(Add.author)
async def process_author(message: Message, state: FSMContext) -> None:
    await state.update_data(author=message.text)
    await state.set_state(Add.published)
    await message.answer("Введите год издания:")


@add_router.message(Add.published)
async def process_published(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(published=message.text)
    data = await state.get_data()
    await state.clear()
    result = await db.add(session=session, title=data.get('title'), author=data.get('author'),
                          published=data.get('published'))
    await message.answer(f"{result}")


@list_router.message(Command("list"))
async def cmd_list(message: Message, session: AsyncSession) -> None:
    result = await db.list_books(session=session)
    if result:
        for book in result:
            st = "Название: " + book[0] + " Автор: " + book[1] + " Дата публикации: " + book[2].strftime(
                '%Y')
            if book[3] is not None:
                st += " (удалена);"
            else:
                st += ";"
            await message.answer(text=st)


delete_router = Router()


@delete_router.message(Command("delete"))
async def cmd_delete(message: Message, state: FSMContext) -> None:
    await state.set_state(Delete.title_delete)
    await message.answer("Введите название книги:")


@delete_router.message(Delete.title_delete)
async def process_title_delete(message: Message, state: FSMContext) -> None:
    await state.update_data(title_delete=message.text)
    await state.set_state(Delete.author_delete)
    await message.answer("Введите автора:")


@delete_router.message(Delete.author_delete)
async def process_author_delete(message: Message, state: FSMContext) -> None:
    await state.update_data(author_delete=message.text)
    await state.set_state(Delete.published_delete)
    await message.answer("Введите год издания:")


@delete_router.message(Delete.published_delete)
async def process_published(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(published_delete=message.text)
    data = await state.get_data()
    exists_row = await db.select_for_delete(session=session, title=data.get('title_delete'),
                                            author=data.get('author_delete'),
                                            published=data.get('published_delete'))
    if exists_row:
        await state.set_state(Delete.user_answer)
        # response_db = await db.delete(session=session, title=data.get('title_delete'),
        #                               author=data.get('author_delete'),
        #                               published=data.get('published_delete'))
        await message.answer(
            f"Найдена книга: {exists_row[0][0]} {exists_row[0][1]} {exists_row[0][2].strftime('%Y')} удаляем?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="да"),
                        KeyboardButton(text="нет"),
                    ]
                ],
                resize_keyboard=True,
            ),

        )
    else:
        await state.clear()
        await message.answer(text="Книга не найдена")


@delete_router.message(Delete.user_answer, F.text.casefold() == "нет")
async def process_dont_delete_book(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Книга на своей полке!",
        reply_markup=ReplyKeyboardRemove(),
    )


@delete_router.message(Delete.user_answer, F.text.casefold() == "да")
async def process_like_write_bots(message: Message, state: FSMContext, session: AsyncSession) -> None:
    print("IN yes")
    data = await state.get_data()
    await state.clear()
    response_db = await db.delete(session=session, title=data.get('title_delete'),
                                  author=data.get('author_delete'),
                                  published=data.get('published_delete'))
    await message.reply(
        f"{response_db}",
        reply_markup=ReplyKeyboardRemove(),
    )


find_router = Router()


@find_router.message(Command("find"))
async def cmd_borrow(message: Message, state: FSMContext) -> None:
    await state.set_state(Find.title_find)
    await message.answer("Введите название книги:")


@find_router.message(Find.title_borrow)
async def process_title_borrow(message: Message, state: FSMContext) -> None:
    await state.update_data(title_find=message.text)
    await state.set_state(Find.author_find)
    await message.answer("Введите автора:")


@find_router.message(Find.author_find)
async def process_author_borrow(message: Message, state: FSMContext) -> None:
    await state.update_data(author_find=message.text)
    await state.set_state(Borrow.published_borrow)
    await message.answer("Введите год издания:")


@find_router.message(Find.published_find)
async def process_published_borrow(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(published_find=message.text)
    data = await state.get_data()
    await state.clear()
    db_response = await db.find(
        session=session, title=data.get('title_borrow'),
        author=data.get('author_borrow'),
        published=data.get('published_borrow')
    )
    await message.answer(text=f"{db_response}")


borrow_router = Router()


@borrow_router.message(Command("borrow"))
async def cmd_borrow(message: Message, state: FSMContext) -> None:
    await state.set_state(Borrow.title_borrow)
    await message.answer("Введите название книги:")


@borrow_router.message(Borrow.title_borrow)
async def process_title_borrow(message: Message, state: FSMContext) -> None:
    await state.update_data(title_borrow=message.text)
    await state.set_state(Borrow.author_borrow)
    await message.answer("Введите автора:")


@borrow_router.message(Borrow.author_borrow)
async def process_author_borrow(message: Message, state: FSMContext) -> None:
    await state.update_data(author_borrow=message.text)
    await state.set_state(Borrow.published_borrow)
    await message.answer("Введите год издания:")


@borrow_router.message(Borrow.published_borrow)
async def process_published_borrow(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(published_borrow=message.text)
    data = await state.get_data()
    exists_row = await db.select_for_delete(
        session=session, title=data.get('title_borrow'),
        author=data.get('author_borrow'),
        published=data.get('published_borrow')
    )
    if exists_row:
        await state.set_state(Borrow.user_answer_borrow)
        await message.answer(
            f"Найдена книга: {exists_row[0][0]} {exists_row[0][1]} {exists_row[0][2].strftime('%Y')} берем?",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="да"),
                        KeyboardButton(text="нет"),
                    ]
                ],
                resize_keyboard=True,
            ),

        )
    else:
        await state.clear()
        await message.answer(text="Книга не найдена")


@borrow_router.message(Borrow.user_answer_borrow, F.text.casefold() == "нет")
async def process_dont_borrow_book(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Книга на своей полке!",
        reply_markup=ReplyKeyboardRemove(),
    )


@borrow_router.message(Borrow.user_answer_borrow, F.text.casefold() == "да")
async def process_like_borrow_book(message: Message, state: FSMContext, session: AsyncSession) -> None:
    data = await state.get_data()
    await state.clear()
    data_book_id = await db.select_book_id_date_deleted(
        session=session,
        title=data.get("title_borrow"),
        author=data.get("author_borrow"),
    )
    response_db = "Книга удалена!"
    if data_book_id:
        response_db = await db.borrow(
            session=session,
            book_id=data_book_id[0],
            date_start=datetime.now().strftime("%Y-%m-%d"),
            # date_end=data.get("date_end_borrow"),
            user_id=message.from_user.id
        )
    await message.reply(
        f"{response_db}",
        reply_markup=ReplyKeyboardRemove(),
    )


retrieve_router = Router()


@retrieve_router.message(Command("retrieve"))
async def cmd_retrieve(message: Message, state: FSMContext):
    await state.set_state(Retrieve.title_retrieve)
    await message.answer("Введите название книги")


@retrieve_router.message(Retrieve.title_retrieve)
async def process_retrieve_title(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(title_retrieve=message.text)
    await state.set_state(Retrieve.author_retrieve)
    await message.answer("Введите автора издания")


@retrieve_router.message(Retrieve.author_retrieve)
async def process_retrieve_author(message: Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(author_retrieve=message.text)
    data = await state.get_data()
    await state.clear()
    book_id = await db.select_book_id_date_deleted(
        session=session, title=data["title_retrieve"],
        author=data["author_retrieve"]
    )
    response_db = "Нету книги!"
    if book_id:
        response_db = await db.retrieve(
            session=session,
            book_id=book_id[0],
            user_id=message.from_user.id
        )
    await message.answer(f"{response_db}")


async def main():
    engine = create_async_engine(url=config.db_url, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    # Setup dispatcher and bind routers to it
    dp = Dispatcher()
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    # Automatically reply to all callbacks
    # dp.callback_query.middleware(CallbackAnswerMiddleware())

    # Register handlers
    dp.include_router(router)
    dp.include_router(add_router)
    dp.include_router(list_router)
    dp.include_router(delete_router)
    dp.include_router(borrow_router)
    dp.include_router(retrieve_router)
    # dp.include_router(callbacks.router)

    # Set bot commands in UI
    # await set_ui_commands(bot)
    commands = await bot.get_my_commands()
    if commands:
        await bot.delete_my_commands()
    await set_default_commands(bot)

    # Run bot
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
