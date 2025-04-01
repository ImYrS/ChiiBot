from enum import Enum

from aiogram.filters.callback_data import CallbackData


class Action(str, Enum):
    DELETE = "delete"


class TopicCallback(CallbackData, prefix="topic"):
    action: Action
    topic_id: int
