import config
import database as db
import keyboards as kb
from aiogram import Bot, Dispatcher, executor
from aiogram.types import CallbackQuery, Message

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)


@dp.callback_query_handler(lambda callback: callback.data == 'help')
async def process_help(callback_query: CallbackQuery):
    HELP_INFO = """Some help info"""
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=HELP_INFO)


@dp.callback_query_handler(lambda callback: callback.data == 'show_tracklist')
async def process_show_tracklist(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=db.Song.show_tracklist())


@dp.message_handler()
async def send_greeting(msg: Message):
    await msg.reply('Что вы хотите выбрать?', reply_markup=kb.KB_MAIN)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
