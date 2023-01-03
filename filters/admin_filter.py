from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from config.config import admin
class IsAdmin(BoundFilter):
    admins_list = admin
    async def check(self, message: types.Message) -> bool:
        return message.from_user.id == int(self.admins_list)