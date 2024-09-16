from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

user_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✖️ Отменить", callback_data="cancel")
        ]
    ]
)