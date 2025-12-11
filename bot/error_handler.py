import logging
import os
import traceback
import requests
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

DISCORD_ERROR_WEBHOOK_URL = os.getenv("DISCORD_ERROR_WEBHOOK_URL")


def _safe_snippet(value: object, max_len: int = 900) -> str:
    """Convertit en str et tronque proprement."""
    try:
        text = str(value)
    except Exception:
        text = "<unserializable>"
    if len(text) > max_len:
        return text[: max_len - 20] + "... (truncated)"
    return text


def send_discord_log_embed(
    title: str,
    update_str: str,
    chat_data: str,
    user_data: str,
    traceback_str: str,
) -> None:
    if not DISCORD_ERROR_WEBHOOK_URL:
        return

    embed = {
        "title": title,
        "color": 0xE74C3C,
        "fields": [
            {
                "name": "Update",
                "value": _safe_snippet(update_str),
                "inline": False,
            },
            {
                "name": "Chat data",
                "value": _safe_snippet(chat_data),
                "inline": False,
            },
            {
                "name": "User data",
                "value": _safe_snippet(user_data),
                "inline": False,
            },
            {
                "name": "Traceback",
                "value": _safe_snippet(traceback_str),
                "inline": False,
            },
        ],
    }

    payload = {
        "content": "",      # tu peux mettre @here si tu veux ping
        "embeds": [embed],
    }

    try:
        requests.post(
            DISCORD_ERROR_WEBHOOK_URL,
            json=payload,
            timeout=5,
        )
    except Exception as e:
        logger.error("Erreur lors de l'envoi du log Discord: %s", e)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log l'erreur et l'envoie sur Discord via webhook."""
    logger.error("Exception while handling an update:", exc_info=context.error)

    tb_string = "".join(
        traceback.format_exception(
            None, context.error, context.error.__traceback__
        )
    )

    if isinstance(update, Update):
        try:
            update_str = update.to_dict()
        except Exception:
            update_str = update
    else:
        update_str = update

    send_discord_log_embed(
        title="[SAETL Bot] Erreur Telegram",
        update_str=update_str,
        chat_data=context.chat_data,
        user_data=context.user_data,
        traceback_str=tb_string,
    )