import database as db
import keyboards as kb
from states import OrderStates

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message


async def send_greeting(msg: Message):
    """Send keyboard with options 'help', 'show_tracklist', 'order'."""

    await msg.answer(text='Что вы хотите выбрать?', reply_markup=kb.KB_MAIN)


async def show_help(callback_query: CallbackQuery):
    """Send help information as message from the Bot to user,
    when user chose 'help'."""

    HELP_INFO = """Отправьте боту любое сообщение. Выберите нужную команду.
    """
    await callback_query.message.answer(text=HELP_INFO)
    await callback_query.answer()


async def show_tracklist(callback_query: CallbackQuery):
    """Send tracklist as message from the Bot to user,
    when user chose 'show_tracklist'."""

    await callback_query.message.answer(text=db.Song.show_tracklist())
    await callback_query.answer()


async def start_ordering(callback_query: CallbackQuery):

    await callback_query.message.answer(text='Введите номер песни')
    await OrderStates.choose_song_number.set()
    await callback_query.answer()


async def process_song_id_invalid(msg: Message):
    """If entered song id not exists."""

    text = (f'Неверный номер песни, попробуйте снова.'
            f'Введите число от 1 до {len(db.Song.select())}')
    return await msg.answer(text=text)


async def process_song_id(msg: Message, state: FSMContext):
    """Chose song id from tracklist."""

    await state.update_data(chosen_song_id=int(msg.text))
    await OrderStates.enter_congratulation.set()
    await msg.answer('Введите текст позравления')


async def enter_congratulation(msg: Message, state: FSMContext):
    """Enter congratulation text, song is choosen."""

    await state.update_data(congratulation=msg.text)
    user_data = await state.get_data()
    msg_text = ('Заказ на поздравление создано\n'
                f'Выбранная песня:{user_data["chosen_song_id"]}'
                f'\nПоздравление:\n{user_data["congratulation"]}')
    await msg.answer(text=msg_text)
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_greeting)
    dp.register_callback_query_handler(show_help, lambda callback:
        callback.data == 'help', state='*')
    dp.register_callback_query_handler(show_tracklist,
        lambda callback: callback.data == 'show_tracklist', state='*')
    dp.register_callback_query_handler(start_ordering,
        lambda callback: callback.data == 'order', state='*')
    dp.register_message_handler(process_song_id_invalid,
        lambda msg: not msg.text.isdigit() or
        int(msg.text) not in [song.id for song in db.Song.select()],
        state=OrderStates.choose_song_number)
    dp.register_message_handler(process_song_id,
        state=OrderStates.choose_song_number)
    dp.register_message_handler(enter_congratulation,
        state=OrderStates.enter_congratulation)
