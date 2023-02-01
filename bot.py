# -*- coding: utf-8 -*-
from config.config import admin
from loader import bot, dp
from sql import create_db
from handlers import client_handler, admin_handler, moderator_handler
from aiogram.utils import executor
import asyncio
import filters


async def on_startup(dp):
	await asyncio.sleep(10)
	await create_db()
	await bot.send_message(admin, "Бот запущен")


async def on_shutdown(dp):
	await bot.close()


filters.setup(dp)
client_handler.register_handlers_clients(dp)
admin_handler.register_handlers_admin(dp)
moderator_handler.register_handlers_moderator(dp)


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)