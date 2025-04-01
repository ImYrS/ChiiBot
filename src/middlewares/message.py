"""Message related middlewares."""

from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message, TelegramObject

from src import config
from src.database import ForwardMessage
from src.types import SendBy


class MessageRecorderMiddleware(BaseMiddleware):
    """Middleware to save message metadata into db."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: Dict[str, Any],
    ):
        send_by = SendBy.HOST if message.from_user.id == config.ADMIN_ID else SendBy.GUEST
        current_message = await ForwardMessage.create(
            user=data["user"],
            from_message_id=message.message_id,
            from_chat_id=message.chat.id,
            send_by=send_by,
        )

        data["current_message"] = current_message

        return await handler(message, data)


class MessageReplyMiddleware(BaseMiddleware):
    """Middleware to get reply message metadata if exists."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: Dict[str, Any],
    ):
        reply_message = None

        if message.reply_to_message:
            reply_message = (
                # Reply to others' message
                await ForwardMessage.get_or_none(
                    to_message_id=message.reply_to_message.message_id,
                    to_chat_id=message.chat.id,
                )
                if message.reply_to_message.from_user.id != message.from_user.id
                # Reply to self
                else await ForwardMessage.get_or_none(
                    from_message_id=message.reply_to_message.message_id,
                    from_chat_id=message.chat.id,
                    user=data["user"],
                )
            )

        data["reply_message"] = reply_message

        return await handler(message, data)
