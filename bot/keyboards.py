from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Buttons for InlineKeyboards
BTN_ORDER = InlineKeyboardButton('Заказать поздравление',
    callback_data='order')
BTN_TRACKLIST = InlineKeyboardButton('Показать треклист',
    callback_data='show_tracklist')
BTN_HELP = InlineKeyboardButton('Помощь по боту',
    callback_data='help')
BTN_TO_SONG_CHOSING = InlineKeyboardButton('К выбору песни',
    callback_data='choose_song')
BTN_TO_ENTER_CONGR = InlineKeyboardButton('К вводу поздравления',
    callback_data='choose_congratulation')
BTN_APPROVE = InlineKeyboardButton('Подтвердить',
    callback_data='approve')

# InlineKeyboards
KB_MAIN = InlineKeyboardMarkup(row_width=1).add(BTN_ORDER,
                                                BTN_TRACKLIST,
                                                BTN_HELP)
KB_FROM_ENTER_CONGR = InlineKeyboardMarkup(row_width=1).add(
    BTN_TO_SONG_CHOSING)
KB_FROM_ORDER_APPROVAL = InlineKeyboardMarkup(row_width=1).add(
    BTN_TO_SONG_CHOSING, BTN_TO_ENTER_CONGR, BTN_APPROVE)
