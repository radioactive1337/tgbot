from aiogram import types, Router
from aiogram.filters import CommandStart, Command

user_router = Router()


@user_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"hi, {message.chat.username}")


@user_router.message(Command('ex', 'names'))
async def menu_cmd(message: types.Message):
    await message.answer("here is...")


@user_router.message()
async def message(message: types.Message):
    await message.answer(message.text)
