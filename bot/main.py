import config
import database as db
import keyboards as kb
from states import OrderStates
from aiogram import Bot, Dispatcher, executor
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler()
async def send_greeting(msg: Message):
    """Send keyboard with options 'help', 'show_tracklist', 'order'."""

    await msg.answer(text='Что вы хотите выбрать?', reply_markup=kb.KB_MAIN)


@dp.callback_query_handler(lambda callback: callback.data == 'help')
async def show_help(callback_query: CallbackQuery):
    """Send help information as message from the Bot to user,
    when user chose 'help'."""

    HELP_INFO = """Отправьте боту любое сообщение. Выберите нужную команду.
    """
    await callback_query.message.answer(text=HELP_INFO)
    await callback_query.answer()


@dp.callback_query_handler(lambda callback: callback.data == 'show_tracklist',
                           state='*')
async def show_tracklist(callback_query: CallbackQuery):
    """Send tracklist as message from the Bot to user,
    when user chose 'show_tracklist'."""

    await callback_query.message.answer(text=db.Song.show_tracklist())
    await callback_query.answer()


@dp.callback_query_handler(lambda callback: callback.data == 'order',
                           state='*')
async def start_ordering(callback_query: CallbackQuery):
    """Chose song id from tracklist."""

    await callback_query.message.answer(text='Введите номер песни')
    await OrderStates.choose_song_number.set()
    await callback_query.answer()


@dp.message_handler(lambda msg: int(msg.text) not in [song.id for song in db.Song.select()],
                    state=OrderStates.choose_song_number)
async def process_song_id_invalid(msg: Message):
    """If entered song id not exists."""

    text = f'Неверный номер песни, попробуйте снова. Введите число от 1 до {len(db.Song.select())}'
    return await msg.answer(text=text)


@dp.message_handler(state=OrderStates.choose_song_number)
async def process_song_id(msg: Message, state: FSMContext):

    await state.update_data(chosen_song_id=int(msg.text))
    await OrderStates.enter_congratulation.set()
    await msg.answer('Введите текст позравления')


@dp.message_handler(state=OrderStates.enter_congratulation)
async def enter_congratulation(msg: Message, state: FSMContext):
    """Enter congratulation text, song is choosen."""

    await state.update_data(congratulation=msg.text)
    user_data = await state.get_data()
    msg_text = f'Выбранная песня:{user_data["chosen_song_id"]}\nПоздравление:\n{user_data["congratulation"]}'
    await msg.answer(text=msg_text)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
