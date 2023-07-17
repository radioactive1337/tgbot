import asyncio
import aioschedule
import telebot
import logging

from requests import Session
from datetime import datetime
from telebot import types
from telebot.async_telebot import AsyncTeleBot

from bot_data import token
from bot_data import cmc_api_key

bot = AsyncTeleBot(token)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
now = datetime.now()
current_time = now.strftime("%H:%M")


def market_gatherer():
    url = "https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': f'{cmc_api_key}',
    }
    session = Session()
    session.headers.update(headers)
    req = session.get(url)
    data = req.json()
    total_market_cap = float(data.get("data").get("quote").get("USD").get("total_market_cap"))
    total_volume_24h = float(data.get("data").get("quote").get("USD").get("total_volume_24h"))
    total_mcap_percentage_change = float(
        data.get("data").get("quote").get("USD").get("total_market_cap_yesterday_percentage_change"))
    btc_dominance = float(data.get("data").get("btc_dominance"))
    return (f"market cap   -->   {'{0:,}'.format(round(total_market_cap)).replace(',', ' ')}\n"
            f"24h volume   -->   {'{0:,}'.format(round(total_volume_24h)).replace(',', ' ')}\n"
            f"mcap change %   -->   {'{0:,}'.format(round(total_mcap_percentage_change, 3)).replace(',', ' ')}\n"
            f"btc dominance   -->   {'{0:,}'.format(round(btc_dominance, 3)).replace(',', ' ')}")


def news_gatherer():
    pass


async def send_market_info(chat_id) -> None:
    await bot.send_message(chat_id, market_gatherer())


@bot.message_handler(commands=["start"])
async def send_welcome(message):
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/start', '/xxx', '/xxx')
    start_markup.row('/market', '/stop', '/token')
    await bot.reply_to(message, "Hi!", reply_markup=start_markup)


@bot.message_handler(commands=["market"])
async def set_market_timer(message):
    aioschedule.every(4).day.at("9:30").do(send_market_info, message.chat.id)


@bot.message_handler(commands=["news"])
async def set_news_timer(message):
    pass


@bot.message_handler(commands=["stop"])
async def stop_scheduler(m):
    await bot.send_message(m.chat.id, "stopping market sender")
    aioschedule.cancel_job(aioschedule.jobs[0])


async def scheduler():
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(bot.infinity_polling(), scheduler())


if __name__ == "__main__":
    asyncio.run(main())
