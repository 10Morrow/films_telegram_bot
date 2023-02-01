import asyncio
from aiogram import types
from typing import List
from aiogram.types import InlineKeyboardMarkup


class SenderList:
    def __init__(self, bot, db):
        self.bot = bot
        self.connector = db

    async def get_keyboard(self, text_button, url_button):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text=text_button, url=url_button))
        return keyboard

    async def get_users(self, name_camp):
        results_query = await self.connector.get_user_list(name_camp)
        return [result.get('user_id') for result in results_query]

    async def update_status(self, table_name, user_id, status, description):
        await self.connector.update_status(table_name, user_id, status, description)

    async def send_message(self, user_id: int, from_chat_id: int, message_id: int, name_camp: str, keyboard: InlineKeyboardMarkup = None):
        try:
            await self.bot.copy_message(user_id, from_chat_id, message_id, reply_markup=keyboard)
        except Exception as e:
            await asyncio.sleep(5)
            await self.update_status(name_camp, user_id, 'unsuccessful', f'{e}')
            return await self.send_message(user_id, from_chat_id, message_id, name_camp, keyboard)
        else:
            await self.update_status(name_camp, user_id, 'success', 'No errors')
            return True
        return False

    async def broadcaster(self, name_camp: str, from_chat_id: int, message_id: int, text_button: str = None, url_button: str = None):
        keyboard = None

        if text_button and url_button:
            keyboard = await self.get_keyboard(text_button, url_button)

        users_ids = await self.get_users(name_camp)
        count = 0
        try:
            for user_id in users_ids:
                if await self.send_message(int(user_id), from_chat_id, message_id, name_camp, keyboard):
                    count += 1
                await asyncio.sleep(.06)
        finally:
            print(f"Разослали сообщение {count} пользователям")

        return count
