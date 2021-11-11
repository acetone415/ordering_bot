from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Buttons for InlineKeyboards
BTN_ORDER = InlineKeyboardButton('Заказать поздравление',
                                 callback_data='order')
BTN_TRACKLIST = InlineKeyboardButton('Показать треклист',
                                     callback_data='show_tracklist')
BTN_HELP = InlineKeyboardButton('Помощь по боту',
                                callback_data='help')

# InlineKeyboards
KB_MAIN = InlineKeyboardMarkup(row_width=1).add(BTN_ORDER,
                                                BTN_TRACKLIST,
                                                BTN_HELP)
