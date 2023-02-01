from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from database.db_manager import DataBase

db = DataBase()


def check_sub_keyboard(links):
    keyboard = types.InlineKeyboardMarkup()
    if links:
        for link in links:
            keyboard.add(types.InlineKeyboardButton(text="Подписаться", url=link[0]))
    keyboard.add(types.InlineKeyboardButton(text="Проверить", callback_data="check_subscribe"))
    return keyboard


def get_confirm_button_keyboard():
    keyboard_builder = types.InlineKeyboardMarkup()
    keyboard_builder.add(types.InlineKeyboardButton(text='Добавить кнопку', callback_data='button_add'))
    keyboard_builder.add(types.InlineKeyboardButton(text='Продолжить без кнопки', callback_data='button_no'))
    return keyboard_builder


def url_link_for_ad(text, url):
    added_keyboards = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, url=url)]])
    return added_keyboards

def confirm_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Подтвердить', callback_data='sender_confirm'))
    keyboard.add(types.InlineKeyboardButton(text='Отмена', callback_data='sender_cancel'))
    return keyboard