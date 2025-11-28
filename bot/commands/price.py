from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_price_usd


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Usage: /price bitcoin")
        return
    coin_id = context.args[0].lower()
    try:
        price_value = get_price_usd(coin_id)
        await update.message.reply_text(f"Prix de {coin_id} : {price_value:.4f} $")
    except Exception as e:
        await update.message.reply_text(f"Erreur pour {coin_id} : {e}")
