from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from models.models import DataBase

buttons: list[KeyboardButton] = [
    KeyboardButton(text=i[0]) for i in DataBase().get_all_categorys()
]

categorys_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[buttons],
    resize_keyboard=True
)

yes_or_no_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Нет'),
            KeyboardButton(text='Да'),
        ]
    ],
    resize_keyboard=True
)
