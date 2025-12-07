from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_ohlc  # tu l'utilises déjà pour /chart


def classify_trend(prices: list[float]) -> str:
    if len(prices) < 2:
        return "données insuffisantes"

    start = prices[0]
    end = prices[-1]
    change_pct = (end - start) / start * 100

    if change_pct >= 10:
        return f"forte tendance haussière (+{change_pct:.1f} %)"
    if change_pct >= 3:
        return f"tendance haussière modérée (+{change_pct:.1f} %)"
    if change_pct <= -10:
        return f"forte tendance baissière ({change_pct:.1f} %)"
    if change_pct <= -3:
        return f"tendance baissière modérée ({change_pct:.1f} %)"
    return f"marché plutôt neutre ({change_pct:.1f} %)"


async def tendance7(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /tendance7 [coin]  -> par défaut bitcoin
    coin = (context.args[0].lower() if context.args else "bitcoin")

    try:
        # on récupère 7 jours de clôtures via ton service existant
        df = get_ohlc(coin, days=7, interval="daily")
    except Exception as e:
        await update.message.reply_text(f"🚨 Erreur données de marché : {e}")
        return

    if df.empty or "close" not in df.columns:
        await update.message.reply_text("⚠️ Impossible de récupérer l'historique 7 jours.")
        return

    closes = df["close"].tolist()
    summary = classify_trend(closes)

    await update.message.reply_text(
        f"📈 Tendance sur 7 jours pour {coin} :\n👉 {summary}\n"
        "ℹ️ Indication de tendance uniquement, pas de conseil d’investissement."
    )
