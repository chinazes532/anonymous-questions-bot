from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram.utils.deep_linking import create_start_link


import keyboards.builder as bkb
import keyboards.inline as ikb

from states.ask_state import AskState
from states.callback_ask import CallbackAskState

from database import (add_user, get_user,
                      insert_message, get_user_id_by_ref_id)

user = Router()

TEXT = """
🚀 Здесь можно отправить анонимное сообщение человеку, который опубликовал эту ссылку

🖊 Напишите сюда всё, что хотите ему передать, и через несколько секунд он получит ваше сообщение, но не будет знать от кого

Отправить можно фото, видео, 💬 текст, 🔊 голосовые, 📷 видеосообщения (кружки), а также ✨ стикеры"""


@user.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    ref_link = command.args

    link = await create_start_link(bot, user_id, encode=True)

    ref_id = link.split('start=')[-1]

    await add_user(user_id, link, ref_id)

    user = await get_user(user_id)

    if ref_link:
        ref_id_from_link = ref_link.split('start=')[-1]

        referral = await get_user_id_by_ref_id(ref_id_from_link)
        if referral:
            user_referral_id = referral[0]
            await message.answer(text=TEXT,
                                 reply_markup=ikb.user_cancel)
            await state.update_data(ref_link=user_referral_id)
            await state.set_state(AskState.ask)
        else:
            await message.answer("Неверная реферальная ссылка.")
            await state.clear()
    else:
        await message.answer(f"Начните получать анонимные вопросы прямо сейчас!\n\n"
                             f"👉 {user[1]}\n\n"
                             f"Разместите эту ссылку ☝️ в описании своего профиля Telegram, TikTok, Instagram (stories), чтобы вам могли написать 💬",
                             reply_markup=await bkb.menu(user_id))
        await state.clear()


@user.message(AskState.ask)
async def ask(message: Message, state: FSMContext, bot: Bot):
    if len(message.text) > 4000:
        return await message.reply("Слишком длинное сообщение.")
    else:
        await state.update_data(ask=message.text)
        data = await state.get_data()

        ref_link = data.get("ref_link")
        ask = data.get("ask")
        user_id = message.from_user.id
        try:
            await bot.send_message(chat_id=ref_link,
                                   text=f'🔔 У тебя новое сообщение!\n\n'
                                        f'<blockquote>{ask}</blockquote>\n\n'
                                        f'↩️ Свайпни для ответа.',
                                   parse_mode='HTML')
            await message.answer("Сообщение отправлено, ожидайте ответ!",
                                 reply_markup=await bkb.ask_menu(ref_link))
            await insert_message(message.message_id, user_id)

            await state.clear()


        except Exception as e:
            if "Telegram server says - Forbidden: bot was blocked by the user" in str(e):
                await message.answer("Пользователь заблокировал бота.\n"
                                     "Отправить сообщение невозможно.")


@user.message(CallbackAskState.callback_ask)
async def ask(message: Message, state: FSMContext, bot: Bot):
    if len(message.text) > 4000:
        return await message.reply("Слишком длинное сообщение.")

    await state.update_data(callback_ask=message.text)
    data = await state.get_data()

    ref_link = data.get("ref_link")
    ask = data.get("callback_ask")  # Assuming this should be 'callback_ask'

    # Check if ref_link is valid
    if ref_link is None:
        return await message.reply("Ошибка: не удалось получить ссылку.")

    try:
        await bot.send_message(chat_id=ref_link,
                               text=f'🔔 У тебя новое сообщение!\n\n'
                                    f'<blockquote>{ask}</blockquote>\n\n'
                                    f'↩️ Свайпни для ответа.',
                               parse_mode='HTML')

        await message.answer("Сообщение отправлено, ожидайте ответ!",
                             reply_markup=await bkb.ask_menu(ref_link))

        await state.clear()

    except Exception as e:
        if "Telegram server says - Forbidden: bot was blocked by the user" in str(e):
            await message.answer("Пользователь заблокировал бота.\n"
                                 "Отправить сообщение невозможно.")


@user.callback_query(F.data.startswith("write_more_"))
async def write_more(callback: CallbackQuery, state: FSMContext):
    ref_link = callback.data.split("_")[2]
    await state.update_data(ref_link=ref_link)
    await callback.message.answer(text=TEXT,
                                  reply_markup=ikb.user_cancel)
    await state.set_state(CallbackAskState.callback_ask)
