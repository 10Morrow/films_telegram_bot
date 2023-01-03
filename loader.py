# -*- coding: utf-8 -*-
import asyncio
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from sql import create_pool
from config import config

storage = MemoryStorage()
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


loop = asyncio.get_event_loop()
db = loop.run_until_complete(create_pool())
