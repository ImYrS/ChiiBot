from enum import IntEnum, StrEnum


class SettingKey(StrEnum):
    """Enum for settings."""

    CORE_ADMIN_ID = "core.admin_id"
    CORE_GROUP_ID = "core.group_id"

    FEAT_FORWARD_MODE = "feat.forward_mode"


class SettingType(IntEnum):
    """Enum for setting type."""

    STRING = 0
    INTEGER = 1
    BOOLEAN = 2
    JSON = 3
