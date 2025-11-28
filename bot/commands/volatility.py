from telegram import Update
from telegram.ext import ContextTypes

import pandas as pd

from ..services import get_ohlc
from ..indicators import compute_volatility


async def volatility(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /volatility bitcoin 30")
        return
    coin_id = context.args[0].lower()
    days = int(context.args[1])
    try:
        ohlc = get_ohlc(coin_id, days)
    except Exception as e:
        await update.message.reply_text(f"Erreur API : {e}")
        return
    closes = [row[4] for row in ohlc]
    close_series = pd.Series(closes)
    vol = compute_volatility(close_series)
    await update.message.reply_text(f"Volatilité annualisée approx. sur {days}j : {vol:.2f} %")
