from telegram import Update
from telegram.ext import ContextTypes

import pandas as pd

from ..services import get_ohlc
from ..indicators import compute_volatility


async def volatility(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text(
            "📊 Usage :\n"
            "➡️ /volatility bitcoin 30"
        )
        return

    coin_id = context.args[0].lower()
    days_str = context.args[1]

    # Vérifier que days est bien un entier
    try:
        days = int(days_str)
    except ValueError:
        await update.message.reply_text(
            f"⚠️ Nombre de jours invalide : {days_str}\n"
            "Exemple : /volatility bitcoin 30"
        )
        return

    try:
        ohlc = get_ohlc(coin_id, days)
    except Exception as e:
        await update.message.reply_text(f"🚨 Erreur API pour {coin_id} : {e}")
        return

    if not ohlc:
        await update.message.reply_text(
            f"⚠️ Impossible de récupérer les données pour {coin_id}."
        )
        return

    closes = [row[4] for row in ohlc]
    close_series = pd.Series(closes)
    vol = compute_volatility(close_series)

    await update.message.reply_text(
        f"📉 Volatilité annualisée approximative sur {days} jours pour {coin_id} : {vol:.2f} %"
    )
