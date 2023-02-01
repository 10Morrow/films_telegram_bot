# -*- coding: utf-8 -*-
from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from loader import bot, dp, db


class DataBase:
	pool: Connection = db

	ADD_NEW_USER = "INSERT INTO bot_users(user_id, subscribe) VALUES ($1, False)"

	IS_USER_EXIST = "SELECT * FROM bot_users WHERE user_id = $1"

	USER_SUBSCRIBED = "SELECT subscribe FROM bot_users WHERE user_id = $1"

	SUB_UPDATE = "UPDATE bot_users SET subscribe = $1 WHERE user_id = $2"

	MODERATORS_LIST = "SELECT * FROM moderators"

	ADD_NEW_POST = "INSERT INTO films(film_id, film_photo_id, film_name, film_link) VALUES ($1, $2, $3, $4)"

	RETURN_POST = "SELECT (film_photo_id, film_name, film_link) FROM films WHERE film_id = $1"

	POST_EXIST = "SELECT * FROM films WHERE film_id = $1"

	DELETE_POST = "DELETE FROM films WHERE film_id = $1"

	ADD_MODERATOR = "INSERT INTO moderators(moderator_id) VALUES ($1)"

	DELETE_MODERATOR = "DELETE FROM moderators WHERE moderator_id = $1"

	IS_MODERATOR = "SELECT * FROM moderators WHERE moderator_id = $1"

	FILMS_LIST = "SELECT (film_id, film_photo_id, film_name, film_link) FROM films"

	GET_USERS = "SELECT subscribe FROM bot_users"

	ADD_NEW_LINK = "INSERT INTO partners_links(link) VALUES ($1)"

	GET_LINKS = "SELECT link FROM partners_links"

	DEL_LINK = "DELETE FROM partners_links WHERE link = $1"

	UPDATE_STATUS = "UPDATE $1 SET status=$2, description=$3 WHERE user_id=$4"

	CREATE_TABLE = "CREATE TABLE $1 (user_id bigint NOT NULL, status text, description text, PRIMARY KEY (user_id))"

	async def add_new_user(self, user_id):
		try:
			await self.pool.fetchval(self.ADD_NEW_USER, user_id)
		except UniqueViolationError:
			pass

	async def is_user_exist(self, user_id):
		result = await self.pool.fetchval(self.IS_USER_EXIST, user_id)
		return bool(result)

	async def user_subscribed(self, user_id):
		result = await self.pool.fetchval(self.USER_SUBSCRIBED, user_id)
		return result

	async def change_sub_status(self,user_id, status):
		args = status, user_id
		await self.pool.fetchval(self.SUB_UPDATE, *args)

	async def add_new_post(self, film_id, photo_id, film_name, film_link):
		args = film_id, photo_id, film_name, film_link
		try:
			await self.pool.fetchval(self.ADD_NEW_POST, *args)
		except UniqueViolationError:
			pass

	async def return_post(self, post_id):
		result = await self.pool.fetchval(self.RETURN_POST, post_id)
		return result

	async def post_id_exist(self, post_id):
		result = await self.pool.fetchval(self.POST_EXIST, post_id)
		return bool(result)

	async def del_post(self, post_id):
		try:
			await self.pool.fetchval(self.DELETE_POST, post_id)
		except UniqueViolationError:
			pass


	async def is_moderator(self, moderator_id):
		result = await self.pool.fetchval(self.IS_MODERATOR, moderator_id)
		return bool(result)

	async def add_moderator(self, moderator_id):
		try:
			await self.pool.fetchval(self.ADD_MODERATOR, moderator_id)
		except UniqueViolationError:
			pass

	async def del_moderator(self, moderator_id):
		try:
			await self.pool.fetchval(self.DELETE_MODERATOR, moderator_id)
		except UniqueViolationError:
			pass

	async def get_films_list(self):
		result = await self.pool.fetch(self.FILMS_LIST)
		result = [i['row'] for i in result]
		if type(result) != list:
			result = [result]
		return result

	async def get_users(self):
		true_user, false_user = 0, 0
		result = await self.pool.fetch(self.GET_USERS)
		for i in result:
			if i[0]:
				true_user += 1
			else:
				false_user += 1
		result_text = f"Subscribed users : {true_user}\nUnsubscribed users : {false_user}"
		return result_text

	async def add_new_link(self, link):
		try:
			await self.pool.fetchval(self.ADD_NEW_LINK, link)
		except UniqueViolationError:
			pass

	async def get_links(self):
		result = await self.pool.fetch(self.GET_LINKS)
		return result

	async def del_link(self, link):
		try:
			await self.pool.fetchval(self.DEL_LINK, link)
		except UniqueViolationError:
			pass

	async def check_table(self, name_camp):
		CHECK_TABLE = f"""SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = '{name_camp}');"""
		result = await self.pool.fetchval(CHECK_TABLE)
		return bool(result)

	async def create_table(self, name_camp):
		print(name_camp)
		CREATE_TABLE = f"CREATE TABLE {name_camp} (user_id bigint NOT NULL, status text, description text, PRIMARY KEY (user_id));"
		INSERT_DATA = f"INSERT INTO {name_camp} (user_id, status, description) SELECT user_id, 'waiting', null FROM bot_users;"
		try:
			await self.pool.execute(CREATE_TABLE)
			await self.pool.execute(INSERT_DATA)
		except UniqueViolationError:
			pass

	async def delete_table(self, name_camp):
		DROP_TABLE = f"DROP TABLE {name_camp}"
		await self.pool.fetchval(DROP_TABLE)

	async def get_user_list(self, name_camp):
		GET_USERS_LIST = f"SELECT user_id FROM {name_camp} WHERE status = 'waiting'"
		result = await self.pool.fetch(GET_USERS_LIST)
		return result

	async def update_status(self, table_name, user_id, status, description):
		UPDATE_STATUS = f"UPDATE {table_name} SET status='{status}', description='{description}' WHERE user_id={user_id}"
		await self.pool.fetchval(UPDATE_STATUS)