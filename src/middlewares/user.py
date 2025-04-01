"""User related middlewares."""

from typing import Any, Awaitable, Callable, Dict

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject

from src.database import User


class UserMiddleware(BaseMiddleware):
    """Middleware to inject user object into handler data."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        user, created = await User.get_or_create(
            user_id=event.from_user.id,
            defaults={
                "username": event.from_user.username,
            },
        )
        data["user"] = user
        data["is_new_user"] = created

        return await handler(event, data)
