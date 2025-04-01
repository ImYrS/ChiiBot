"""
Forward router

This router is used to handle message forwarding.
"""

from typing import Optional

from aiogram import F, Router
from aiogram.types import Message
from aiogram.types.reaction_type_emoji import ReactionTypeEmoji
from aiogram.utils.i18n import gettext as _
from tortoise.exceptions import DoesNotExist

from src import config, topic
from src.database import ForwardMessage, User
from src.errors import Templates as ErrorTemplates
from src.errors import send_topic_invalid
from src.middlewares import MessageRecorderMiddleware, MessageReplyMiddleware
from src.types import ForwardMode, SendBy
from src.utils import is_acceptable_message

router = Router()

router.message.middleware(MessageRecorderMiddleware())
router.message.middleware(MessageReplyMiddleware())


async def forward_message_common(
    message: Message,
    to_chat_id: int,
    message_thread_id: Optional[int],
    current_message: ForwardMessage,
    reply_message: Optional[ForwardMessage],
    send_by: SendBy,
) -> Optional[Message]:
    """
    Common message forwarding function to handle forwarding logic.

    :param message: Original message
    :param to_chat_id: Target chat ID
    :param message_thread_id: Target topic ID
    :param current_message: Current message record
    :param reply_message: Reply message record
    :param send_by: Sender type

    :return: Forwarded new message, or None if forwarding failed
    """
    if not is_acceptable_message(message):
        return None

    reply_to_message_id = None
    if reply_message:
        reply_to_message_id = (
            reply_message.from_message_id
            if reply_message.send_by != send_by
            else reply_message.to_message_id
        )

    if config.FORWARD_MODE == ForwardMode.FORWARD:
        new_message = await message.bot.forward_message(
            chat_id=to_chat_id,
            message_thread_id=message_thread_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
        )
    else:
        new_message = await message.send_copy(
            chat_id=to_chat_id,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
        )

    current_message.to_message_id = new_message.message_id
    current_message.to_chat_id = new_message.chat.id
    await current_message.save()

    await message.bot.set_message_reaction(
        chat_id=message.chat.id,
        message_id=message.message_id,
        reaction=[ReactionTypeEmoji(emoji="🕊")],
    )

    return new_message


@router.message(F.chat.type == "private")
async def forward_to_admin(
    message: Message,
    user: User,
    current_message: ForwardMessage,
    reply_message: Optional[ForwardMessage],
) -> None:
    """
    Handle private messages

    Forward guest's message to specified topic in group.
    """
    if not config.GROUP_ID:
        return

    # Cannot forward to self, unless it's in debug mode
    if user.user_id == config.ADMIN_ID and not config.DEBUG:
        await message.answer(
            ErrorTemplates.COMMON.format(
                msg=_("You cannot forward messages to yourself.")
            ),
        )
        return

    if not user.topic_id:
        topic_id = await topic.create_for_user(message.bot, user)
        if topic_id == -1:
            await message.answer(
                ErrorTemplates.COMMON.format(msg=_("Failed to create topic."))
            )
            return

        await message.bot.send_message(
            chat_id=config.GROUP_ID,
            message_thread_id=user.topic_id,
            text=_(
                "<b>User Info</b>\n\n"
                "<b>User ID:</b> <a href='tg://user?id={user_id}'>{user_id}</a>\n"
                "<b>Username:</b> <code>{username}</code>\n"
                "<b>Name:</b> <i>{full_name}</i>"
            ).format(
                user_id=message.from_user.id,
                username=message.from_user.username or _("Not Set"),
                full_name=message.from_user.full_name,
            ),
        )

    if user.message_available_count == 0:
        await message.answer(
            ErrorTemplates.COMMON.format(
                msg=_(
                    "You can only send a maximum of 2 messages before the admin replies to you."
                )
            )
        )
        return

    if user.blocked:
        await message.bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[ReactionTypeEmoji(emoji="👎")],
        )
        return

    if not is_acceptable_message(message):
        await message.answer(
            ErrorTemplates.COMMON.format(
                msg=_("This message type does not support forwarding.")
            ),
            reply_to_message_id=message.message_id,
        )
        return

    new_message = await forward_message_common(
        message=message,
        to_chat_id=config.GROUP_ID,
        message_thread_id=user.topic_id,
        current_message=current_message,
        reply_message=reply_message,
        send_by=SendBy.GUEST,
    )

    if not new_message:
        return

    user.message_available_count -= 1 if user.message_available_count != -1 else 0
    await user.save()

    if user.tutorial_step == 0:
        tutorial_msg = await message.answer(
            _(
                "Great! <b>That 🕊 reaction means your message has been successfully forwarded to my admin.</b> "
                "So you can clearly know exactly if I'm working properly.\n"
                "Wishing you a wonderful day!\n\n"
                "<blockquote>This notice won't be shown again.</blockquote>"
            ),
            reply_to_message_id=message.message_id,
        )
        await message.bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=tutorial_msg.message_id,
            reaction=[ReactionTypeEmoji(emoji="🍾")],
        )

        user.tutorial_step = 1
        await user.save()


@router.message(F.is_topic_message)
async def forward_to_guest(
    message: Message,
    current_message: ForwardMessage,
    reply_message: Optional[ForwardMessage],
) -> None:
    """
    Handle group messages

    Forward the message back to guest.
    Only messages from admin will be forwarded.
    """
    if message.from_user.id != config.ADMIN_ID or message.chat.id != config.GROUP_ID:
        return

    if not is_acceptable_message(message):
        # Ignore non-acceptable messages in group
        # This is to prevent forwarding some service messages like new chat members.
        return

    try:
        guest = await User.get(topic_id=message.message_thread_id)
    except DoesNotExist:
        await send_topic_invalid(message)
        return

    await forward_message_common(
        message=message,
        to_chat_id=guest.user_id,
        message_thread_id=None,
        current_message=current_message,
        reply_message=reply_message,
        send_by=SendBy.HOST,
    )

    if guest.message_available_count >= 0:
        guest.message_available_count = -1
        await guest.save()
