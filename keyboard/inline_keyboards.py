from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

btn = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text="vnature knopka", callback_data="top_up")]]
    )

def check_sub_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Подписаться", url="https://t.me/enot_films"))
    keyboard.add(types.InlineKeyboardButton(text="Проверить", callback_data="check_subscribe"))
    return keyboard