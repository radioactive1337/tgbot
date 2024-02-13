from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f

from filters.chat_types import ChatType

user_router = Router()
user_router.message.filter(ChatType(['private']))


@user_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"hi, {message.chat.username}")


@user_router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer("here is...menu")


@user_router.message(or_f(Command('stats'), (F.text.lower().contains('stat') | F.text.lower().contains('стат'))))
async def menu_cmd(message: types.Message):
    await message.answer("here is...statistics!")


@user_router.message(~(F.text.lower().contains('test')) | F.text.lower().contains('qq'))
async def message(message: types.Message):
    await message.answer('xd')
