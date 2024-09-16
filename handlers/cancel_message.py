from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database import get_user

import keyboards.builder as bkb

cancel_fsm = Router()


@cancel_fsm.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    user_id = callback.from_user.id
    user = await get_user(user_id)
    await callback.answer()
    await state.clear()
    await callback.message.answer(f"Начните получать анонимные вопросы прямо сейчас!\n\n"
                                  f"👉 {user[1]}\n\n"
                                  f"Разместите эту ссылку ☝️ в описании своего профиля Telegram, TikTok, Instagram (stories), чтобы вам могли написать 💬",
                                  reply_markup=await bkb.menu(user_id))
