import json
from typing import Any, Optional, Union

from tortoise.exceptions import DoesNotExist

from src.database import Setting
from src.types import SettingKey, SettingType


async def get(key: SettingKey, default: Optional[Any] = None) -> Optional[Any]:
    """
    Get the value of a setting from the database.

    :param key: Setting key
    :param default: default value to return if the setting does not exist
    :return: Setting value or default value
    """
    try:
        setting = await Setting.get(key=key)

        if setting.type_ == SettingType.INTEGER:
            return int(setting.value)

        elif setting.type_ == SettingType.BOOLEAN:
            return setting.value.lower() == "true"

        elif setting.type_ == SettingType.JSON:
            return json.loads(setting.value)

        return setting.value

    except DoesNotExist:
        return default


async def update(
    key: SettingKey,
    value: Union[str, int, bool, dict],
    create_if_not_exists: bool = True,
) -> bool:
    """
    Update the value of a setting in the database.

    :param key: Setting key
    :param value: Setting value
    :param create_if_not_exists: Whether to create the setting if it does not exist
    :return: True if the setting was updated or created, False otherwise
    """
    try:
        setting = await Setting.get(key=key)

        setting.value = value
        await setting.save()

        return True

    except DoesNotExist:
        if create_if_not_exists:
            await Setting.create(key=key, value=value)
            return True

        return False
