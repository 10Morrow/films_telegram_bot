from loader import bot, dp
from config import config
from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.db_manager import DataBase
from BuisnessLogic.sender import SenderList
from filters.admin_filter import IsAdmin
from keyboard.inline_keyboards import get_confirm_button_keyboard, url_link_for_ad, confirm_keyboard
db = DataBase()
sender = SenderList(bot, db)
class AdminPanel(StatesGroup):
    id = State()
    photo = State()
    name = State()
    link = State()

class AdCompany(StatesGroup):
    get_message = State()
    q_button = State()
    get_text_button = State()
    get_url_button = State()
    sender_decide = State()



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


async def get_sender(message: types.Message, state: FSMContext):
    wrong_letter = "!@#$%^&*()_+=-№;:?.,/|\\"
    try:
        company_name = message.text.split(' ')[-1]
        for i in wrong_letter:
            if i in company_name or len(company_name) > 10 or company_name.isdigit() or company_name[0].isdigit():
                await message.answer('Имя не может содержать только цифры или спец. символы')
                return
    except:
        await message.answer('Некоректный ввод')
        return
    await message.answer(f'Приступаем создавать кампанию для рассылки. Имя кампании - {company_name}\r\n\r\n'
                         f'Отправь мне сообщение, которое будет использовано как рекламное')

    await state.update_data(company_name=company_name)
    await state.set_state(AdCompany.get_message)


async def get_message(message: types.Message, state: FSMContext):
    await message.answer(f'Ok, я запомнил сообщение, которое ты хочешь разослать.\r\n'
                         f'Кнопку будем добавлять?', reply_markup=get_confirm_button_keyboard())
    await state.update_data(message_id=message.message_id, chat_id=message.from_user.id)
    await state.set_state(AdCompany.q_button)

async def q_button(call: CallbackQuery, state: FSMContext):
    if call.data == 'button_add':
        await call.message.answer(f'Отправь текст для кнопки.', reply_markup=None)
        await state.set_state(AdCompany.get_text_button)
    elif call.data == 'button_no':
        await call.message.edit_reply_markup(reply_markup=None)
        data = await state.get_data()
        message_id = int(data.get('message_id'))
        chat_id = int(data.get('chat_id'))
        await confirm(call.message, message_id, chat_id)
        await state.set_state(AdCompany.sender_decide)

    await call.answer()


async def get_text_button(message: types.Message, state: FSMContext):
    await state.update_data(text_button=message.text)
    await message.answer(f'Теперь отправь ссылку')
    await state.set_state(AdCompany.get_url_button)


async def get_url_button(message: types.Message, state: FSMContext):
    await state.update_data(url_button=message.text)
    data = await state.get_data()
    text = data.get('text_button')
    url = message.text
    added_keyboards = url_link_for_ad(text, url)
    data = await state.get_data()
    message_id = int(data.get('message_id'))
    chat_id = int(data.get('chat_id'))
    await confirm(message, message_id, chat_id, added_keyboards)
    await state.set_state(AdCompany.sender_decide)


async def confirm(message: types.Message, message_id, chat_id, reply_markup=None):
    await bot.copy_message(chat_id, chat_id, message_id, reply_markup=reply_markup)
    await message.answer('Вот сообщение, которое будет отправлено. Подтверди.',reply_markup = confirm_keyboard())


async def sender_decide(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    message_id = data.get('message_id')
    chat_id = data.get('chat_id')
    text_button = data.get('text_button')
    url_button = data.get('url_button')
    name_camp = str(data.get('company_name'))

    if call.data == 'sender_confirm':
        await call.message.edit_text(f'Начинаю рассылку', reply_markup=None)
        if not await db.check_table(name_camp):
            await db.create_table(name_camp)
        count = await sender.broadcaster(name_camp, chat_id, message_id, text_button, url_button)
        await call.message.answer(f'Успешно разослали рекламное сообщение [{count}] пользователям')
        await db.delete_table(name_camp)

    elif call.data == 'sender_cancel':
        await call.message.edit_text('Отменил рассылку', reply_markup=None)
    await state.finish()
    await call.answer()


async def admin_commands(message: types.Message):
    if message.text.startswith('/help'):
        await bot.send_message(message.from_user.id, "/upload\n/add_moderator id \n/del_moderator id\n"
                                                     "/user_count\n"
                                                     "/print_films_list\n/del_post №_of_post\n/add_link\n"
                                                     "/del_link\n/ad_post")
    if message.text.startswith('/add_moderator'):
        try:
            admin_message = message.text.split(' ')
            moderator_id = admin_message[-1]
            await db.add_moderator(int(moderator_id))
        except:
            await bot.send_message(message.from_user.id, "Некоректный ввод")
    elif message.text.startswith('/del_moderator'):
        try:
            admin_message = message.text.split(' ')
            moderator_id = admin_message[-1]
            await db.del_moderator(int(moderator_id))
        except:
            await bot.send_message(message.from_user.id, "Некоректный ввод")
    elif message.text.startswith('/user_count'):
        users = await db.get_users()
        await bot.send_message(message.from_user.id, users)
    elif message.text.startswith('/print_films_list'):
        films_list = await db.get_films_list()
        for i in films_list:
            text = f"№ {i[0]}\n" + "Фильм: " + str(i[2]) + "\n" + "Фильм тут 👉" + str(i[3])
            await bot.send_photo(chat_id=message.chat.id, photo=i[1], caption=text)

    elif message.text.startswith('/del_post'):
        try:
            post = message.text.split(' ')
            post_id = post[-1]
            await db.del_post(int(post_id))
        except:
            await bot.send_message(message.from_user.id, "Некоректный ввод")
    elif message.text.startswith('/add_link'):
        try:
            link = message.text.split(' ')[-1]
            await db.add_new_link(link)
        except:
            await bot.send_message(message.from_user.id, "Некоректный ввод")

    elif message.text.startswith('/del_link'):
        try:
            link = message.text.split(' ')[-1]
            await db.del_link(link)
        except:
            await bot.send_message(message.from_user.id, "Некоректный ввод")



def register_handlers_admin(dp: Dispatcher):

    dp.register_message_handler(get_sender, IsAdmin(), commands=["ad_post"], state = None)
    dp.register_message_handler(get_message, IsAdmin(), content_types=["text", "photo"], state=AdCompany.get_message)
    dp.register_callback_query_handler(q_button, IsAdmin(), text_startswith='button', state=AdCompany.q_button)
    dp.register_message_handler(get_text_button, IsAdmin(), content_types=["text"], state=AdCompany.get_text_button)
    dp.register_message_handler(get_url_button, IsAdmin(), content_types=["text"], state=AdCompany.get_url_button)
    dp.register_callback_query_handler(sender_decide, IsAdmin(), text_startswith='sender', state=AdCompany.sender_decide)

    dp.register_message_handler(start_create_post, IsAdmin(), commands=["upload"], state = None)
    dp.register_message_handler(enter_id, IsAdmin(), content_types=["text"], state = AdminPanel.id)
    dp.register_message_handler(load_photo, IsAdmin(), content_types=["photo"], state=AdminPanel.photo)
    dp.register_message_handler(enter_name, IsAdmin(), content_types=["text"], state=AdminPanel.name)
    dp.register_message_handler(enter_link, IsAdmin(), content_types=["text"], state=AdminPanel.link)

    dp.register_message_handler(admin_commands, IsAdmin(), content_types=["text"], text_startswith='/')