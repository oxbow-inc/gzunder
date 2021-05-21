
from gzunder.settings import settings
import logging
from textwrap import dedent

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

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


@dp.message_handler(commands='meet')
async def cmd_meet(message: types.Message):
    # Set state
    await Form.title.set()

    await message.answer(dedent("""
        Чтобы создать встречу, мне нужно кое-что узнать...
        Как озаглавим нашу встречу? Выбери что-то цепляющее,
        например "Хочу поиграть в шахматы"
    """))


@dp.message_handler(lambda message: len(message.text) > 2, state=Form.title)
async def process_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text

    await Form.next()
    await message.answer(dedent("""
        Напишите строчку о себе, например "кмс по шахматам UwU"
    """))


@dp.message_handler(lambda message: not len(message.text) > 2, state=Form.title)
async def process_title_empty(message: types.Message):
    await message.answer(dedent("""
        Потрудись написать более-менее содержательный заголовок.
        Итак, как назовем наше мероприятие?
    """))


@dp.message_handler(state=Form.whoami)
async def process_whoami(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['whoami'] = message.text

    await Form.next()
    await message.answer(dedent("""
        Напишите что для вас важно, кого вы ищете.
        Например "Не пишите мне, если вы не знаете
        что такое королевский гамбит"
    """))


@dp.message_handler(state=Form.whoru)
async def process_whoru(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['whoru'] = message.text

    await Form.next()
    await message.answer(dedent("""
        Напишите более развернутое описание.
        Например: "С проигравшего - пицца"
    """))


@dp.message_handler(state=Form.description)
async def process_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Погнали", "Отмена")

    await Form.next()
    # And send message
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Давай удостоверимся что все так:'),
            md.text(),
            md.text(md.bold(data['title'])),
            md.text(md.bold('Кто я:'), data['whoami']),
            md.text(md.bold('Кто ты:'), data['whoru']),
            md.text(data['description']),
            md.text(),
            md.text('Публикуем?'),
            sep='\n',
        ),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN,
    )


@dp.message_handler(lambda message: message.text not in ["Погнали", "Отмена"], state=Form.accept)
async def process_accept_invalid(message: types.Message):
    return await message.answer(dedent("""
        Выбери с клавиатуры.
    """))


@dp.message_handler(state=Form.accept)
async def process_accept_yes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['accept'] = message.text

    # Remove keyboard
    markup = types.ReplyKeyboardRemove()

    if message.text == "Погнали":
        print(data)
        await message.answer(dedent("""
            Анкета отправлена!.. в stdout
        """), reply_markup=markup)
    else:
        await message.answer(dedent("""
            Ну нет так нет, чего бухтеть-то.
        """), reply_markup=markup)

    # Finish conversation
    await state.finish()


# # Check age. Age gotta be digit
# @dp.message_handler(lambda message: not message.text.isdigit(), state=Form.age)
# async def process_age_invalid(message: types.Message):
#     return await message.answer(dedent("""
#         Вводи свой возраст цифрами. Я же тупой бот.
#         Итак, сколько тебе лет?
#     """))


# @dp.message_handler(lambda message: message.text.isdigit(), state=Form.age)
# async def process_age(message: types.Message, state: FSMContext):
#     # Update state and data
#     await Form.next()
#     await state.update_data(age=int(message.text))

#     # Configure ReplyKeyboardMarkup
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
#     markup.add("Male", "Female")
#     markup.add("Other")

#     await message.answer("What is your gender?", reply_markup=markup)


# @dp.message_handler(lambda message: message.text not in ["Male", "Female", "Other"], state=Form.gender)
# async def process_gender_invalid(message: types.Message):
#     """
#     In this example gender has to be one of: Male, Female, Other.
#     """
#     return await message.answer("Bad gender title. Choose your gender from the keyboard.")


# @dp.message_handler(state=Form.gender)
# async def process_gender(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['gender'] = message.text

#         # Remove keyboard
#         markup = types.ReplyKeyboardRemove()

#         # And send message
#         await bot.send_message(
#             message.chat.id,
#             md.text(
#                 md.text('Hi! Nice to meet you,', md.bold(data['title'])),
#                 md.text('Age:', md.code(data['age'])),
#                 md.text('Gender:', data['gender']),
#                 sep='\n',
#             ),
#             reply_markup=markup,
#             parse_mode=ParseMode.MARKDOWN,
#         )

#     # Finish conversation
#     await state.finish()


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
