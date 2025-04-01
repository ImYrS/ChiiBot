import os

from dotenv import load_dotenv

from src import setting
from src.types import ForwardMode, SettingKey

load_dotenv()

BOT_TOKEN = os.getenv("CORE_BOT_TOKEN")
GROUP_ID = None
ADMIN_ID = None

FORWARD_MODE = ForwardMode(os.getenv("FEAT_FORWARD_MODE", "copy"))

DEBUG = bool(os.getenv("DEV_DEBUG", False))


async def reload():
    global GROUP_ID, ADMIN_ID
    GROUP_ID = await setting.get(SettingKey.CORE_GROUP_ID)
    ADMIN_ID = await setting.get(SettingKey.CORE_ADMIN_ID)
