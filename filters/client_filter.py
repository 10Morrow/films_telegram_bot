from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from database.db_manager import DataBase

db = DataBase()
class SubClient(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return await db.user_subscribed(message.from_user.id)