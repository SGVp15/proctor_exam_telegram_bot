from aiogram import types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

from Telegram.config import USERS_ID, ADMIN_ID, LOG_FILE, TEMPLATE_FILE_XLSX
from Telegram.keybords.inline import inline_kb_main
from Telegram.main import dp, bot
from Telegram.Call_Back_Data import CallBackData as call_back


def is_empty_file(file) -> bool:
    with open(file=file, mode="r", encoding='utf-8') as f:
        s = f.read()
    return len(s) <= 10


@dp.message(Command('id'))
async def send_id(message: types.Message):
    await message.answer(str(message.chat.id))


@dp.callback_query(
    F.data.in_({call_back.get_log, call_back.get_log_program, call_back.get_template_file_xlsx})
    & F.from_user.id.in_({*ADMIN_ID, *USERS_ID})
)
async def get_file(callback_query: types.callback_query):
    query = callback_query.data
    file = LOG_FILE
    if query == call_back.get_log_program:
        file = FSInputFile(TEMPLATE_FILE_XLSX, 'template_file.xlsx')
    elif query == call_back.get_log:
        file = FSInputFile(LOG_FILE, 'log_file.txt')
    elif query == call_back.get_template_file_xlsx:
        file = FSInputFile(TEMPLATE_FILE_XLSX, 'template_file.xlsx')

    # try:
    #     if is_empty_file(file):
    #         await bot.answer_callback_query(chat_id=callback_query.from_user.id, text=f'✅ Файл пустой',
    #                                         reply_markup=inline_kb_main)
    # except UnicodeDecodeError:
    #     ...
    await bot.send_document(chat_id=callback_query.from_user.id, document=file, reply_markup=inline_kb_main)
