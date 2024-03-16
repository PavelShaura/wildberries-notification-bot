from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


subscribe: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", callback_data="sub")]
    ]
)