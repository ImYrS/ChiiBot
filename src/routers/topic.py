"""
Topic router

This router is used to handle topic-related actions.
"""

from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from src import config, topic
from src.types import Action, TopicCallback

router = Router()


@router.callback_query(TopicCallback.filter(F.action == Action.DELETE))  # type: ignore
async def delete_topic(query: CallbackQuery, callback_data: TopicCallback) -> None:
    """
    Handle topic-related callback queries

    This handler is used to handle topic-related callback queries.
    """
    if query.from_user.id != config.ADMIN_ID:
        await query.answer(_("Permission denied"), show_alert=True)
        return

    await query.answer(_("Deleting topic..."))
    if not await topic.delete(bot=query.bot, topic_id=callback_data.topic_id):
        await query.answer(_("Failed to delete topic"), show_alert=True)
