from aiogram import Bot

from src import config
from src.database import User


async def create_for_user(bot: Bot, user: User) -> int:
    """Create a TOPIC in group and associate it with the user."""
    topic_name = f"{user.user_id}"
    if user.username:
        topic_name += f" @{user.username}"

    topic = await bot.create_forum_topic(chat_id=config.GROUP_ID, name=topic_name)

    if not topic.message_thread_id:
        return -1

    user.topic_id = topic.message_thread_id
    await user.save()

    return topic.message_thread_id


async def delete(bot: Bot, topic_id: int) -> bool:
    """Delete the TOPIC."""
    return await bot.delete_forum_topic(chat_id=config.GROUP_ID, message_thread_id=topic_id)
