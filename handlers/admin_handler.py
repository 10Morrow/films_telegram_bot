from loader import bot, dp
from config import config
from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.db_manager import DataBase
from filters.admin_filter import IsAdmin

db = DataBase()

class AdminPanel(StatesGroup):
    id = State()
    photo = State()
    name = State()
    link = State()


async def start_create_post(message: types.Message):
    await AdminPanel.id.set()
    await bot.send_message(message.from_user.id, "Enter film id")


async def enter_id(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        post_exist = await db.post_id_exist(int(message.text))
        if not post_exist:
            async with state.proxy() as data:
                data["id"] = int(message.text)
            await AdminPanel.next()
            await bot.send_message(message.from_user.id, "upload photo")
        else:
            await bot.send_message(message.from_user.id, "This film id already exist")
            return
    else:
        await bot.send_message(message.from_user.id, "enter digit")
        return


async def load_photo(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        async with state.proxy() as data:
            data["photo"] = message.photo[0].file_id
        await AdminPanel.next()
        await bot.send_message(message.from_user.id, "Enter the name of the film")
    else:
        await bot.send_message(message.from_user.id, "Please, upload photo!")
        return

async def enter_name(message: types.Message, state: FSMContext):
    if len(message.text) < config.max_len_of_the_film_name:
        async with state.proxy() as data:
            data["name"] = message.text
        await AdminPanel.next()
        await bot.send_message(message.from_user.id, "Enter the link to the video")
    else:
        await bot.send_message(message.from_user.id, "The name should be shorter than 50 characters")
        return


async def enter_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["link"] = message.text
    async with state.proxy() as data:
        await db.add_new_post(data["id"], data["photo"], data["name"], data["link"])
        text = "Фильм: " + str(data["name"]) + "\n" + "Фильм тут 👉" + str(data["link"])
        await bot.send_photo(chat_id=message.chat.id, photo=data["photo"], caption=text)
    await state.finish()


async def admin_commands(message: types.Message):
    if message.text.startswith('!/help'):
        await bot.send_message(message.from_user.id, "!/add_moderator id \n!/del_moderator id\n"
                                                     "!/user_count\n"
                                                     "!!/print_films_list\n!!/del_post\n")
    if message.text.startswith('!/add_moderator'):
        admin_message = message.text.split(' ')
        moderator_id = admin_message[-1]
        await db.add_moderator(int(moderator_id))
    elif message.text.startswith('!/del_moderator'):
        admin_message = message.text.split(' ')
        moderator_id = admin_message[-1]
        await db.del_moderator(int(moderator_id))
    elif message.text.startswith('!/user_count'):
        users = await db.get_users()
        await bot.send_message(message.from_user.id, users)


def register_handlers_admin(dp: Dispatcher):
	dp.register_message_handler(start_create_post, IsAdmin(), commands=["upload"], state = None)
	dp.register_message_handler(enter_id, IsAdmin(), content_types=["text"], state = AdminPanel.id)
	dp.register_message_handler(load_photo, IsAdmin(), content_types=["photo"], state=AdminPanel.photo)
	dp.register_message_handler(enter_name, IsAdmin(), content_types=["text"], state=AdminPanel.name)
	dp.register_message_handler(enter_link, IsAdmin(), content_types=["text"], state=AdminPanel.link)
	dp.register_message_handler(admin_commands, IsAdmin(), content_types=["text"], text_startswith='!/')