from environs import Env

env = Env()
env.read_env()


TOKEN = env("TOKEN")
DATABASE_NAME = "band.db"
TRACKLIST_NAME = "tracklist.txt"
GROUP_CHANNEL_ID = env("GROUP_CHANNEL_ID")
