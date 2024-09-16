from aiogram import Router, Bot
from aiogram.filters.command import CommandObject, Command
from aiogram.types import Message

from config import ADMIN_ID, GROUP_USERNAME


issue = Router()


@issue.message(Command("issue"))
async def cmd_issue(message: Message, command: CommandObject, bot: Bot):
    if command.args:
        await message.answer(f"✅ Спасибо! Ваше предложение отпрвлено на рассмотрение.\n\n"
                             f"Если ваше сообщение требует ответа, обратитесь в нашу поддержку @{GROUP_USERNAME}", )
        await bot.send_message(ADMIN_ID,
                               f"💡 Новое предложение от @{message.from_user.username}:\n\n"
                               f"{command.args}")
    else:
        await message.answer('💡 Здесь вы можете предложить свою идею по улучшению нашего бота\n\n'
                             'Напишите "<code>/issue Текст...</code>", чтобы отправить нам сообщение',
                             parse_mode="HTML")
