from aiogram import types, Router
from aiogram.filters import CommandStart, Command

user_router = Router()


@user_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(f"hi, {message.chat.username}")


@user_router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer("here is...menu")


@user_router.message(Command('topdex'))
async def menu_cmd(message: types.Message):
    await message.answer("here is...top exchanges")


@user_router.message(Command('toptoken'))
async def menu_cmd(message: types.Message):
    await message.answer("here is...top tokens")


@user_router.message()
async def message(message: types.Message):
    await message.answer(message.text)
