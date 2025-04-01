from enum import IntEnum, StrEnum


class SendBy(IntEnum):
    """Enum for send by."""

    HOST = 0
    GUEST = 1


class ForwardMode(StrEnum):
    """Enum for forward mode."""

    FORWARD = "forward"
    COPY = "copy"
