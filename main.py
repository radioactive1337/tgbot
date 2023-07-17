import asyncio
import aioschedule
import telebot
import logging

from telebot import types
from telebot.async_telebot import AsyncTeleBot

from InfoCollector import InfoCollector
from bot_data import token
from bot_data import coins

bot = AsyncTeleBot(token)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
IC = InfoCollector()


async def send_market_info(chat_id) -> None:
    await bot.send_message(chat_id, IC.market_gatherer())


@bot.message_handler(commands=["start"])
async def send_welcome(message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/start', '/xxx', '/xxx')
    start_markup.row('/market', '/stop', '/crypto')
    await bot.send_message(message.chat.id, "Hi!", reply_markup=start_markup)


@bot.message_handler(commands=['crypto'])
async def command_crypto(message):
    coins_markup = types.InlineKeyboardMarkup(row_width=1)
    for i in coins:
        coins_markup.add(types.InlineKeyboardButton(text=i, callback_data=i))
    await bot.send_message(message.chat.id, "📃 Choose the coin:", reply_markup=coins_markup)


@bot.callback_query_handler(func=lambda call: True)
async def callback_crypto_stocks(call):
    req = call.data.split('_')
    coins_markup = types.InlineKeyboardMarkup(row_width=1)
    for i in coins:
        if req[0] == i:
            continue
        else:
            coins_markup.add(types.InlineKeyboardButton(text=i, callback_data=i))
    await bot.edit_message_text(IC.coin_info_gatherer(symbol=f"{req[0]}"), reply_markup=coins_markup,
                                chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.message_handler(commands=["market"])
async def set_market_timer(message):
    await bot.send_message(message.chat.id, "market sender every day at 9:30")
    aioschedule.every().day.at("9:30").do(send_market_info, message.chat.id)


@bot.message_handler(commands=["stop"])
async def stop_scheduler(message):
    await bot.send_message(message.chat.id, "stopping market sender")
    aioschedule.cancel_job(aioschedule.jobs[0])


async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(bot.infinity_polling(), scheduler())


if __name__ == "__main__":
    asyncio.run(main())
