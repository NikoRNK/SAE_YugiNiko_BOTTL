from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_ohlc
from ..charts import build_price_chart_png


async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /chart bitcoin 7")
        return
    coin_id = context.args[0].lower()
    days = int(context.args[1])
    try:
        ohlc = get_ohlc(coin_id, days)
    except Exception as e:
        await update.message.reply_text(f"Erreur API : {e}")
        return
    file_path = Path("chart_price.png")
    build_price_chart_png(ohlc, file_path)
    await update.message.reply_photo(photo=open(file_path, "rb"))
