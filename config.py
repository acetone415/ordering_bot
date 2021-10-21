from environs import Env

env = Env()
env.read_env()


TOKEN = env("TOKEN")
DATABASE_NAME = "band.db"
