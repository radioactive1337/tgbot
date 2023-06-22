import pytz
import requests
import telebot
from datetime import datetime
from bot_data import token
from data import PRICE_URL


def get_price(crypto):
    request = requests.get(PRICE_URL + str(crypto) + "USDT")
    response = dict(request.json())
    price = round(float(response["price"]), 4)
    symbol = response["symbol"]
    tz = pytz.timezone("UTC")
    date = datetime.now(tz).strftime("%Y-%m-%d\n%H:%M UTC")

    return f"{date}\n{symbol}\n{price}"


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id,
                         "Hello friend!\nWrite the token name to see its price\nExample:    eth, btc or matic")
        bot.send_message(message.chat.id,
                         "Привет, друг!\nНапиши название токена, чтобы увидеть его цену\nПример:  eth, btc или matic")

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        try:
            bot.send_message(message.chat.id, get_price(message.text.upper()))
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, "Damn...Something was wrong...")

    bot.polling()



if __name__ == "__main__":
    telegram_bot(token)
