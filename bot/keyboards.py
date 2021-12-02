from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Buttons for InlineKeyboards
BTN_ORDER = InlineKeyboardButton('Заказать поздравление',
    callback_data='order')
BTN_TRACKLIST = InlineKeyboardButton('Показать треклист',
    callback_data='show_tracklist')
BTN_HELP = InlineKeyboardButton('Помощь по боту',
    callback_data='help')
BTN_SONG = InlineKeyboardButton('К выбору песни',
    callback_data='choose_song')
BTN_CONGR = InlineKeyboardButton('К вводу поздравления',
    callback_data='choose_congratulation')
BTN_APPROVE = InlineKeyboardButton('Подтвердить',
    callback_data='approve')

# InlineKeyboards
KB_MAIN = InlineKeyboardMarkup(row_width=1).add(BTN_ORDER,
                                                BTN_TRACKLIST,
                                                BTN_HELP)
KB_TO_SONG = InlineKeyboardMarkup(row_width=1).add(
    BTN_SONG)
KB_FROM_ORDER_APPROVAL = InlineKeyboardMarkup(row_width=1).add(
    BTN_SONG, BTN_CONGR, BTN_APPROVE)
