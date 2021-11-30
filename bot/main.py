from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
from handlers import register_handlers

bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
register_handlers(dp=dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
