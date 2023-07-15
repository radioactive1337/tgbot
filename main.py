import asyncio
import aioschedule
import requests
import telebot
import logging
from datetime import datetime
from telebot.async_telebot import AsyncTeleBot

from bot_data import token


def get_coin_market(coin):
    request = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}")
    response = dict(request.json()[0])
    name = response.get("name")
    current_price = response.get("current_price")
    market_cap = response.get("market_cap")
    total_volume = response.get("total_volume")
    price_change_24h = response.get("price_change_24h")
    return f"{name}\nprice -> {current_price}\nprice change -> {price_change_24h}" \
           f"\nmkt cap -> {market_cap}\nvolume -> {total_volume}"


bot = AsyncTeleBot(token)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
now = datetime.now()
current_time = now.strftime("%H:%M")


async def send_info(chat_id) -> None:
    await bot.send_message(chat_id, get_coin_market("bitcoin"))
    aioschedule.clear(chat_id)


@bot.message_handler(commands=["start"])
async def send_welcome(message):
    await bot.reply_to(message, "Hi!")


@bot.message_handler(commands=["market"])
async def set_timer(message):
    aioschedule.every(3600).seconds.do(send_info, message.chat.id).tag(message.chat.id)


async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(bot.infinity_polling(), scheduler())


if __name__ == "__main__":
    asyncio.run(main())
