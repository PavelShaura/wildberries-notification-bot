from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить информацию по товару")],
        [KeyboardButton(text="Получить информацию из БД")],
        [KeyboardButton(text="Остановить уведомления")],
    ],
    resize_keyboard=True,
)
