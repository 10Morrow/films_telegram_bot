from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from database.db_manager import DataBase
from config.config import admin
db = DataBase()

class IsModerator(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return await db.is_moderator(message.from_user.id) or int(message.from_user.id) == int(admin)