from aiogram import F, Router, Bot
from aiogram.types import Message

from aiogram.utils.deep_linking import create_start_link

from database import get_message, get_user, add_user

import keyboards.builder as bkb

answer = Router()


@answer.message(F.text)
async def reply(message: Message, bot: Bot):
    if message.reply_to_message:
        replied_message_id = message.reply_to_message.message_id - 1
        reply_message = await get_message(replied_message_id)
        msg = message.text
        await bot.send_message(chat_id=reply_message[1],
                               text=f'🔔 У тебя новое сообщение!\n\n'
                                    f'<blockquote>{msg}</blockquote>\n\n'
                                    f'↩️ Свайпни для ответа.',
                               parse_mode='HTML')
        await message.answer("Сообщение отправлено, ожидайте ответ!",
                             reply_markup=await bkb.ask_menu(reply_message[1]))
    else:
        user_id = message.from_user.id
        user = await get_user(user_id)
        if user:
            await message.answer(f"Начните получать анонимные вопросы прямо сейчас!\n\n"
                                 f"👉 {user[1]}\n\n"
                                 f"Разместите эту ссылку ☝️ в описании своего профиля Telegram, TikTok, Instagram (stories), чтобы вам могли написать 💬",
                                 reply_markup=await bkb.menu(user_id))
        else:
            link = await create_start_link(bot, 'foo', encode=True)
            await add_user(user_id, link)
            await message.answer(f"Начните получать анонимные вопросы прямо сейчас!\n\n")
