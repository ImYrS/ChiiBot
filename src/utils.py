import time
from typing import Optional

from aiogram.enums import ContentType
from aiogram.types import Message


def formatted_time(
    time_stamp: Optional[int] = int(time.time()),
    secure_format: Optional[bool] = False,
) -> str:
    """
    时间戳转换为格式化时间

    :param time_stamp: 需要格式化的 Unix 时间戳
    :param secure_format: 是否需要安全的字符格式
    :return: 格式化后的时间
    """
    return (
        time.strftime("%Y%m%d_%H%M%S", time.localtime(time_stamp))
        if secure_format
        else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_stamp))
    )


def timestamp(ms: Optional[bool] = True) -> int:
    """
    获取当前时间戳

    :param ms: 是否以毫秒为单位
    :return: 时间戳
    """
    return int(time.time()) if not ms else int(time.time() * 1000)


now = timestamp


def is_acceptable_message(message: Message) -> bool:
    """
    Check if the message is acceptable for forwarding.

    Acceptable list:

    - Text
    - Photo
    - Document
    - Video
    - Sticker
    - Animation (GIF)
    - Voice
    - Audio
    """
    if message.content_type not in (
        ContentType.TEXT,
        ContentType.PHOTO,
        ContentType.DOCUMENT,
        ContentType.VIDEO,
        ContentType.STICKER,
        ContentType.ANIMATION,  # GIF
        ContentType.VOICE,
        ContentType.AUDIO,
    ):
        return False

    return True
