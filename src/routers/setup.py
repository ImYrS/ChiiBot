"""
Setup router

This router is used to handle setup command.
All routers in this router will be invalid after setup.
"""

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from tortoise.exceptions import BaseORMException

from src import config
from src.database import Setting
from src.types import SettingKey, SettingType

router = Router()


@router.message(Command("chii_setup"), (F.chat.type == "supergroup"))
async def command_setup(message: Message) -> None:
    """`/chii_setup`"""
    if config.GROUP_ID or config.ADMIN_ID:
        return

    try:
        await Setting.create(
            key=SettingKey.CORE_GROUP_ID,
            value=message.chat.id,
            type_=SettingType.INTEGER,
        )
        await Setting.create(
            key=SettingKey.CORE_ADMIN_ID,
            value=message.from_user.id,
            type_=SettingType.INTEGER,
        )
    except BaseORMException as e:
        logging.error(f"Failed to create settings: {e}")
        await message.answer(
            _("Failed to setup, please check this in logs or try again later."),
            reply_to_message_id=message.message_id,
        )
        return

    await config.reload()

    await message.answer(
        _("Setup completed!\n<code>/chii_setup</code> has been disabled."),
        reply_to_message_id=message.message_id,
    )
