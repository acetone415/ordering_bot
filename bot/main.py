import config
from aiogram import Bot, Dispatcher, executor
from aiogram.types import CallbackQuery, Message
import keyboards as kb


bot = Bot(config.TOKEN)
dp = Dispatcher(bot)


@dp.callback_query_handler(lambda callback: callback.data == 'help')
async def process_help(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Pressed help button')


@dp.message_handler()
async def send_greeting(msg: Message):
    await msg.reply('Что вы хотите выбрать?', reply_markup=kb.kbd_1)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
