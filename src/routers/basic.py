"""
Basic router

This router is used to handle basic commands like /start, /help, /id, etc.
All routes in this router are authentication-free and can be accessed by any user.
"""

from aiogram import Router, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

router = Router()


@router.message(CommandStart(ignore_mention=True))
async def command_start(message: Message) -> None:
    """`/start`"""
    await message.answer(
        _("Hi, I'm <b>{bot_name}</b>.\n\nCommands:\n/id - Get chat and user ID").format(
            bot_name=_("ChiiBot"),
        ),
        reply_to_message_id=message.message_id,
    )


@router.message(Command("id"))
async def command_id(message: Message) -> None:
    """`/id`"""
    await message.answer(
        _(
            "<b>Current Chat</b>\n"
            "id: {chat_id}\n\n"
            "<b>From User</b>\n"
            "id: {user_id}"
        ).format(
            chat_id=html.code(message.chat.id),
            user_id=html.code(message.from_user.id),
        ),
        reply_to_message_id=message.message_id,
    )
