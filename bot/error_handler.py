import logging
import traceback
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log l'erreur et envoie un mail avec les détails."""
    # import tardif pour éviter les imports circulaires
    from .services import send_error_email

    logger.error("Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    if isinstance(update, Update):
        try:
            update_str = str(update.to_dict())
        except Exception:
            update_str = str(update)
    else:
        update_str = str(update)

    subject = "[SAETL Bot] Erreur Telegram"
    body = (
        "Une exception a été levée dans le bot Telegram.\n\n"
        f"Update : {update_str}\n\n"
        f"Chat data : {context.chat_data}\n\n"
        f"User data : {context.user_data}\n\n"
        f"Traceback :\n{tb_string}"
    )

    try:
        send_error_email(subject, body)
    except Exception as e:
        logger.error("Erreur lors de l'envoi du mail d'erreur: %s", e)
