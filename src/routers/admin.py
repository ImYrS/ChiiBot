"""
Admin Router

This router includes commands for admin users, such as /ban, /unban.
"""

from aiogram import F, Router
from aiogram.filters import Command, and_f
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from tortoise.exceptions import DoesNotExist

from src import config
from src.database import User
from src.errors import Templates as ErrorTemplates
from src.errors import send_topic_invalid

router = Router()


@router.message(Command("ban", "block", "unban", "unblock"))
async def command_block(message: Message) -> None:
    """`/ban`, `/block`, `/unban`, `/unblock`"""
    if message.from_user.id != config.ADMIN_ID:
        return

    if not message.is_topic_message:
        await message.answer(
            ErrorTemplates.COMMON.format(
                msg=_("This command is only available in topics.")
            ),
            reply_to_message_id=message.message_id,
        )
        return

    try:
        guest = await User.get(topic_id=message.message_thread_id)
    except DoesNotExist:
        await send_topic_invalid(message)
        return

    block = message.text in ("/ban", "/block")
    if (block and guest.blocked) or (not block and not guest.blocked):
        await message.answer(
            ErrorTemplates.COMMON.format(
                msg=_("This user is already {}.").format(
                    _("blocked") if block else _("unblocked")
                )
            ),
            reply_to_message_id=message.message_id,
        )
        return

    guest.blocked = block
    await guest.save()

    await message.answer(
        _("User #u{user_id} is {status} now.").format(
            user_id=guest.user_id, status=_("blocked") if block else _("unblocked")
        ),
        reply_to_message_id=message.message_id,
    )

    await message.bot.send_message(
        guest.user_id,
        _("You have been {} by admin.\nYour messages {} be processed by me.").format(
            _("blocked") if block else _("unblocked"),
            _("will not") if block else _("will continue to"),
        ),
    )
