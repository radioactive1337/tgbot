from aiogram.types import KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

delete_kb = ReplyKeyboardRemove()

start_kb = ReplyKeyboardBuilder()
start_kb.add(
    KeyboardButton(text='menu'),
    KeyboardButton(text='stats', request_contact=True)
)
start_kb.adjust(2)
