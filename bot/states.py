from aiogram.dispatcher.filters.state import StatesGroup, State


class OrderStates(StatesGroup):

    # States
    choose_song_number = State()
    confirm_song = State()
    enter_congratulation = State()
    confirm_order = State()
