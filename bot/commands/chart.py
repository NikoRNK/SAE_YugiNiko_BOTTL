from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_ohlc
from ..charts import build_price_chart_png


async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text(
            "📊 Usage :\n"
            "➡️ /chart bitcoin 7"
        )
        return

    coin_id = context.args[0].lower()
    days_str = context.args[1]

    # Vérifier que le nombre de jours est un entier
    try:
        days = int(days_str)
    except ValueError:
        await update.message.reply_text(
            f"⚠️ Nombre de jours invalide : {days_str}\n"
            "Exemple : /chart bitcoin 7"
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

    file_path = Path("chart_price.png")
    build_price_chart_png(ohlc, file_path)

    await update.message.reply_photo(
        photo=open(file_path, "rb"),
        caption=f"📈 Graphique des prix sur {days} jours pour {coin_id}"
    )
