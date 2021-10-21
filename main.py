from aiogram import Bot, Dispatcher, executor, types

import config

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_hello(message: types.Message):
    await message.reply('hello')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)