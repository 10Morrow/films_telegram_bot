from loader import dp, bot
from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.db_manager import DataBase
from keyboard.inline_keyboards import check_sub_keyboard
from filters.client_filter import SubClient
from config.config import admin
db = DataBase()


async def start(message : types.Message):
	user_id = message.from_user.id
	await db.add_new_user(user_id)
	await message.answer(f'Приветики, {message.from_user.first_name}!')
	user_channel_status = await bot.get_chat_member(chat_id='@enot_films', user_id=user_id)
	if user_channel_status["status"] != 'left':
		await bot.send_message(message.from_user.id, 'Доступ к фильмам открыт!\n🎬 Введите номер фильма:')
	else:
		await bot.send_message(message.from_user.id, 'Будь добр, подпишись сначала на эти каналаы: ', reply_markup = check_sub_keyboard())


async def answer(message : types.Message):
	user_id = message.from_user.id
	user_channel_status = await bot.get_chat_member(chat_id='@enot_films', user_id=user_id)
	if user_channel_status["status"] != 'left':
		if message.text.isdigit():
			try:
				data = await db.return_post(int(message.text))
				text = "Фильм: " + str(data[1]) + "\n" + "Фильм тут 👉" + str(data[2])
				await bot.send_photo(chat_id=message.chat.id, photo=data[0], caption=text)
			except Exception as ex:
				await bot.send_message(message.from_user.id, 'Такого номера нет 😢')
		else:
			await bot.send_message(message.from_user.id, 'Такого номера нет 😢')
	else:
		await db.change_sub_status(user_id, False)
		await bot.send_message(message.from_user.id, 'Будь добр, подпишись сначала на эти каналаы: ',
						   reply_markup=check_sub_keyboard())

async def answer_pass(message : types.Message):
	await bot.send_message(message.from_user.id, 'Будь добр, подпишись сначала на эти каналаы: ', reply_markup=check_sub_keyboard())


@dp.callback_query_handler(text="check_subscribe")
async def send_random_value(call: types.CallbackQuery):
	user_id = call.message.chat.id
	user_channel_status = await bot.get_chat_member(chat_id='@enot_films', user_id=user_id)
	if user_channel_status["status"] != 'left':
		await db.change_sub_status(user_id, True)
		await call.message.answer('Доступ к фильмам открыт!\n🎬 Введите номер фильма:')
	else:
		await call.message.answer('Дружище, ты так и не подписался...')


async def send_id(message : types.Message):
	user_id = message.from_user.id
	await bot.send_message(admin, f'отпралено службой send_id: {user_id}')
	await bot.send_message(message.from_user.id, 'Ваш id был отправлен администратору.')


def register_handlers_clients(dp : Dispatcher):
	dp.register_message_handler(start, commands = ["start"])
	dp.register_message_handler(send_id, commands = ["send_id"])
	dp.register_message_handler(answer, SubClient(), content_types=["text"])
	dp.register_message_handler(answer_pass, content_types=["text"])