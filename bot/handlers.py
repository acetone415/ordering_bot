from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

import database as db
import keyboards as kb
from states import OrderStates


async def send_greeting(msg: Message):
    """Send keyboard with options 'help', 'show_tracklist', 'order'."""

    await msg.answer(text='Что вы хотите выбрать?', reply_markup=kb.KB_MAIN)


async def show_help(callback_query: CallbackQuery):
    """Send help information as message from the Bot to user,
    when user chose 'help'."""

    HELP_INFO = ('Для начала диалога отправьте боту любое сообщение.\n'
    'Для заказа песни ознакомьтесь с треклистом '
    '(выберете пункт "Показать треклист") и запомните номер нужной песни.\n'
    'Затем выберете пункт "Заказать поздравление" и бот попросит ввести номер '
    'выбранной песни и текст поздравления')
    await callback_query.message.answer(text=HELP_INFO)
    await callback_query.answer()


async def show_tracklist(callback_query: CallbackQuery):
    """Send tracklist as message from the Bot to user,
    when user chose 'show_tracklist'."""

    await callback_query.message.answer(text=db.Song.show_tracklist())
    await callback_query.answer()


async def start_ordering(callback_query: CallbackQuery):

    await callback_query.message.answer(text='Введите номер песни')
    await OrderStates.song.set()
    await callback_query.answer()


async def process_song_id_invalid(msg: Message):
    """If entered song id not exists."""

    text = (f'Неверный номер песни, попробуйте снова.'
            f'Введите число от 1 до {len(db.Song.select())}')
    return await msg.answer(text=text)


async def process_song_id(msg: Message, state: FSMContext,  **kwargs):
    """Chose song id from tracklist."""

    song_id = int(msg.text) if 'song_id' not in kwargs.keys() else\
        kwargs['song_id']
    await state.update_data(chosen_song_id=song_id)
    await OrderStates.congratulation.set()
    await msg.answer(f'Выбранная песня:\n{db.Song[song_id].author} - '
        f'{db.Song[song_id].title}\n'
        'Введите текст позравления:',
        reply_markup=kb.KB_TO_SONG)


async def process_congratulation(msg: Message, state: FSMContext):
    """Entered congratulation text in Message, song is choosen."""

    await state.update_data(congratulation=msg.text)
    user_data = await state.get_data()
    chosen_song_id = user_data['chosen_song_id']
    chosen_song = db.Song[chosen_song_id]
    congratulation = user_data['congratulation']
    msg_text = ('Подтвердите заказ.\n'
                f'Выбранная песня:\n{chosen_song.author} {chosen_song.title}'
                f'\nПоздравление:\n{congratulation}')

    await OrderStates.approve.set()
    await msg.answer(text=msg_text, reply_markup=kb.KB_FROM_ORDER_APPROVAL)


async def approve_order(callback_query: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    db.Order.make_order(song_id=user_data['chosen_song_id'],
        congratulation=user_data['congratulation'])
    await callback_query.message.answer('Заказ на поздравление отправлен')
    await callback_query.answer()
    await state.finish()


async def back_to_song_choosing(callback_query: CallbackQuery):

    await callback_query.answer()
    await start_ordering(callback_query)


async def back_to_congr_choosing(callback_query: CallbackQuery,
                                 state: FSMContext):

    await OrderStates.song.set()
    await callback_query.answer()
    user_data = await state.get_data()
    song_id = user_data['chosen_song_id']
    await process_song_id(msg=callback_query.message, state=state,
        song_id=song_id)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_greeting)

    dp.register_callback_query_handler(show_help, lambda callback:
        callback.data == 'help', state='*')
    dp.register_callback_query_handler(show_tracklist,
        lambda callback: callback.data == 'show_tracklist', state='*')
    dp.register_callback_query_handler(start_ordering,
        lambda callback: callback.data == 'order', state='*')
    dp.register_callback_query_handler(approve_order,
        lambda callback: callback.data == 'approve',
        state=OrderStates.approve)
    dp.register_callback_query_handler(back_to_song_choosing,
        lambda callback: callback.data == 'choose_song',
        state='*')
    dp.register_callback_query_handler(back_to_congr_choosing,
        lambda callback: callback.data == 'choose_congratulation',
        state='*')

    dp.register_message_handler(process_song_id_invalid,
        lambda msg: not msg.text.isdigit() or
        int(msg.text) not in [song.id for song in db.Song.select()],
        state=OrderStates.song)
    dp.register_message_handler(process_song_id,
        state=OrderStates.song)
    dp.register_message_handler(process_congratulation,
        state=OrderStates.congratulation)
