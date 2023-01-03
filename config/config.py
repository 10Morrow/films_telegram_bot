from environs import Env
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

host = env.str("host")

port = env.str("port")

user = env.str("user")

password = env.str("password")

database_name = env.str("database_name")

admin = env.str("main_admin")

max_len_of_the_film_name = 50