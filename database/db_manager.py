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