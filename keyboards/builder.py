from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import get_user


async def menu(user_id):
    user = await get_user(user_id)
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text="🔗 Поделиться ссылкой",
                                url=f"https://t.me/share/url?url=Задай мне анонимный вопрос."
                                     f"\n\n👉{user[1]}"))

    return kb.as_markup()


async def ask_menu(ref_id):
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text="Написать еще ✍️", callback_data=f'write_more_{ref_id}'))

    return kb.as_markup()