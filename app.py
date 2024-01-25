import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Это была команда старт')


@dp.message()
async def echo(message: types.Message):
    text = message.text

    if text in ['test']:
        await message.answer('test')
    else:
        await message.answer(message.text)


async def main():
    await dp.start_polling(bot)


asyncio.run(main())
