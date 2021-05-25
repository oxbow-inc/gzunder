import logging
from textwrap import dedent

import aiogram.utils.markdown as md  # type: ignore[import]
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # type: ignore[import]
from aiogram.dispatcher import FSMContext  # type: ignore[import]
from aiogram.dispatcher.filters import Text  # type: ignore[import]
from aiogram.dispatcher.filters.state import State  # type: ignore[import]
from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.types import ParseMode  # type: ignore[import]
from aiogram.utils import executor

from gzunder.crud import get_client_meetings
from gzunder.crud import init
from gzunder.settings import settings

logging.basicConfig(level=logging.INFO)

API_TOKEN = settings.tg_token


bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    title = State()
    whoami = State()
    whoru = State()
    description = State()
    accept = State()


@dp.message_handler(commands="my")
async def cmd_my(message: types.Message) -> None:
    meetings = await get_client_meetings(client_id=message.chat.id)
    print(meetings)
    if not meetings:
        await message.answer(
            dedent(
                """
            У вас сейчас нет актуальных встреч.
            Чтобы создать встречу, введите /meet.
        """
            )
        )
        return

    await message.answer(
        dedent(
            """
        Ваши встречи:
    """
        )
    )

    for meeting in meetings:
        await message.answer(
            dedent(
                f"""
            {meeting.title}
        """
            )
        )


@dp.message_handler(commands="meet")
async def cmd_meet(message: types.Message) -> None:
    # Set state
    await Form.title.set()

    await message.answer(
        dedent(
            """
        Чтобы создать встречу, мне нужно кое-что узнать...
        Как озаглавим нашу встречу? Выбери что-то цепляющее,
        например "Хочу поиграть в шахматы"
    """
        )
    )


@dp.message_handler(lambda message: len(message.text) > 2, state=Form.title)
async def process_title(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["title"] = message.text

    await Form.next()
    await message.answer(
        dedent(
            """
        Напишите строчку о себе, например "кмс по шахматам UwU"
    """
        )
    )


@dp.message_handler(
    lambda message: not len(message.text) > 2, state=Form.title
)
async def process_title_empty(message: types.Message) -> None:
    await message.answer(
        dedent(
            """
        Потрудись написать более-менее содержательный заголовок.
        Итак, как назовем наше мероприятие?
    """
        )
    )


@dp.message_handler(state=Form.whoami)
async def process_whoami(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["whoami"] = message.text

    await Form.next()
    await message.answer(
        dedent(
            """
        Напишите что для вас важно, кого вы ищете.
        Например "Не пишите мне, если вы не знаете
        что такое королевский гамбит"
    """
        )
    )


@dp.message_handler(state=Form.whoru)
async def process_whoru(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data["whoru"] = message.text

    await Form.next()
    await message.answer(
        dedent(
            """
        Напишите более развернутое описание.
        Например: "С проигравшего - пицца"
    """
        )
    )


@dp.message_handler(state=Form.description)
async def process_description(
    message: types.Message, state: FSMContext
) -> None:
    async with state.proxy() as data:
        data["description"] = message.text

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
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
async def process_accept_invalid(message: types.Message) -> None:
    return await message.answer(
        dedent(
            """
        Выбери с клавиатуры.
    """
        )
    )


@dp.message_handler(state=Form.accept)
async def process_accept_yes(
    message: types.Message, state: FSMContext
) -> None:
    async with state.proxy() as data:
        data["accept"] = message.text

    # Remove keyboard
    markup = types.ReplyKeyboardRemove()

    if message.text == "Погнали":
        print(data)
        await message.answer(
            dedent(
                """
            Анкета отправлена!.. в stdout
        """
            ),
            reply_markup=markup,
        )
    else:
        await message.answer(
            dedent(
                """
            Ну нет так нет, чего бухтеть-то.
        """
            ),
            reply_markup=markup,
        )

    # Finish conversation
    await state.finish()


# You can use state '*' if you need to handle all states
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
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
    await message.answer(
        "Cancelled.", reply_markup=types.ReplyKeyboardRemove()
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=lambda _: init())
