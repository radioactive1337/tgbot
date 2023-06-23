import pytz
import requests
import telebot
from datetime import datetime
from bot_data import token


def get_24hr_data(coin):
    req = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={str(coin).upper()}USDT")
    res = dict(req.json())
    tz = pytz.timezone("UTC")
    date = datetime.now(tz).strftime("%Y-%m-%d %H:%M UTC")
    return (
        f"DATE --> {date}\nNAME --> {res['symbol']}\nPRICE --> {round(float(res['lastPrice']), 4)}\n"
        f"PRICE CHANGE --> {round(float(res['priceChange']), 4)}")


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
            bot.send_message(message.chat.id, get_24hr_data(message.text))
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, "Damn...Something was wrong...")

    bot.polling()


if __name__ == "__main__":
    telegram_bot(token)
