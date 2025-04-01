from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.i18n import lazy_gettext as __

from src.types import Action, TopicCallback


class Templates:
    """Templates for errors"""

    COMMON = __("<b>Error</b>\n\n<blockquote>{msg}</blockquote>")


async def send_topic_invalid(message: Message) -> Optional[Message]:
    """Topic invalid"""
    return await message.answer(
        Templates.COMMON.format(
            msg=__(
                "This Topic is not associated with any guest.\n"
                "We recommend to close/delete this topic."
            )
        ),
        reply_to_message_id=message.message_id,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=str(__("❌ DELETE Topic")),
                        callback_data=TopicCallback(
                            action=Action.DELETE, topic_id=message.message_thread_id
                        ).pack(),
                    )
                ]
            ]
        ),
    )
