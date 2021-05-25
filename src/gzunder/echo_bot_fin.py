"""Main bot source code."""
import logging

import aiogram.utils.markdown as md  # type: ignore[import]
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # type: ignore[import]
from aiogram.dispatcher import FSMContext  # type: ignore[import]
from aiogram.dispatcher.filters import Text  # type: ignore[import]
from aiogram.dispatcher.filters.state import State  # type: ignore[import]
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import Message
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import executor

from gzunder.crud import get_client_meetings
from gzunder.crud import init
from gzunder.settings import settings
from gzunder.settings import talks

logging.basicConfig(level=logging.INFO)

API_TOKEN = settings.tg_token


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()  # TODO Switch to redis
dp = Dispatcher(bot, storage=storage)


# TODO Black-formatted multiline strings are ugly. Fix with a dictionary?

# States
class Form(StatesGroup):
    """The /meet command states"""

    title = State()
    whoami = State()
    whoru = State()
    description = State()
    accept = State()


@dp.message_handler(commands="my")
async def cmd_my(message: Message) -> None:
    """The /my command"""
    meetings = await get_client_meetings(client_id=message.chat.id)
    print(meetings)
    if not meetings:
        await message.answer(talks.my["no_meetings"])
        return

    await message.answer("Ваши встречи:")

    for meeting in meetings:
        await message.answer(f"{meeting.title}")


@dp.message_handler(commands="meet")
async def cmd_meet(message: Message) -> None:
    """The /cmd command, 1st stage: asking title"""
    # Set state
    await Form.title.set()

    await message.answer(talks.meet["title"])


@dp.message_handler(
    lambda message: not len(message.text) > 2, state=Form.title
)
async def process_title_empty(message: Message) -> None:
    """The /cmd command, 1st stage: if title given is too short."""
    await message.answer(talks.meet["invite_too_short"])


@dp.message_handler(lambda message: len(message.text) > 2, state=Form.title)
async def process_title(message: Message, state: FSMContext) -> None:
    """The /cmd command, 2nd stage: asking self description"""
    async with state.proxy() as data:
        data["title"] = message.text

    await Form.next()
    await message.answer(talks.meet["who_am_i"])


@dp.message_handler(state=Form.whoami)
async def process_whoami(message: Message, state: FSMContext) -> None:
    """The /cmd command, 3rd stage: asking mate description"""
    async with state.proxy() as data:
        data["whoami"] = message.text

    await Form.next()
    await message.answer(talks.meet["who_are_you"])


@dp.message_handler(state=Form.whoru)
async def process_whoru(message: Message, state: FSMContext) -> None:
    """The /cmd command, 4th stage: asking extended description."""
    async with state.proxy() as data:
        data["whoru"] = message.text

    await Form.next()
    await message.answer(talks.meet["description"])


@dp.message_handler(state=Form.description)
async def process_description(message: Message, state: FSMContext) -> None:
    """The /cmd command, 5th stage: asking for accept."""
    async with state.proxy() as data:
        data["description"] = message.text

    # Configure ReplyKeyboardMarkup
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Погнали", "Отмена")

    await Form.next()
    # And send message
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text("Давай удостоверимся что все так:"),
            md.text(),
            md.text(md.bold(data["title"])),
            md.text(md.bold("Кто я:"), data["whoami"]),
            md.text(md.bold("Кто ты:"), data["whoru"]),
            md.text(data["description"]),
            md.text(),
            md.text("Публикуем?"),
            sep="\n",
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.message_handler(
    lambda message: message.text not in ["Погнали", "Отмена"],
    state=Form.accept,
)
async def process_accept_invalid(message: Message) -> None:
    return await message.answer(talks.meet["accept_invalid"])


@dp.message_handler(state=Form.accept)
async def process_accept_yes(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["accept"] = message.text

    # Remove keyboard
    markup = ReplyKeyboardRemove()

    if message.text == "Погнали":
        print(data)
        await message.answer(talks.meet["accept_yes"], reply_markup=markup)

    else:
        await message.answer(talks.meet["accept_no"], reply_markup=markup)

    # Finish conversation
    await state.finish()


# You can use state '*' if you need to handle all states
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.answer("Cancelled.", reply_markup=ReplyKeyboardRemove())


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=lambda _: init())
