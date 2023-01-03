# -*- coding: utf-8 -*-
import asyncio
import asyncpg
from config import config


async def create_db():
    create_db_command = open("database/create_database.sql", "r").read()

    conn: asyncpg.Connection = await asyncpg.connect(user=config.user,
                                     password=config.password,
                                     host=config.host,
                                     port=config.port,
                                     database=config.database_name)
    await conn.execute(create_db_command)
    await conn.close()
    print("database created")


async def create_pool():
    return await asyncpg.create_pool(user=config.user,
                                     password=config.password,
                                     host=config.host,
                                     database=config.database_name)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())