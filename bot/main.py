from aiogram import executor

from handlers import register_handlers
from loader import dp


register_handlers(dp=dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
