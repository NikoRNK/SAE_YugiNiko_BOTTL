import numpy as np
from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_ohlc


def summarize_trend(prices: list[float]) -> str:
    if len(prices) < 10:
        return "Pas assez de données pour un résumé fiable."

    n = len(prices)
    thirds = np.array_split(prices, 3)

    parts = []
    labels = ["début de période", "milieu de période", "fin de période"]
    for label, segment in zip(labels, thirds):
        start = float(segment[0])
        end = float(segment[-1])
        change = (end - start) / start * 100
        if change >= 5:
            desc = f"{label} : phase haussière (+{change:.1f} %)."
        elif change <= -5:
            desc = f"{label} : phase baissière ({change:.1f} %)."
        else:
            desc = f"{label} : phase plutôt latérale ({change:.1f} %)."
        parts.append(desc)

    overall_change = (prices[-1] - prices[0]) / prices[0] * 100
    overall = f"Sur toute la période : évolution globale de {overall_change:.1f} %."

    return "\n".join(parts + [overall])


async def simplifie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /simplifie [coin] [jours]  -> ex : /simplifie bitcoin 90
    coin = (context.args[0].lower() if context.args else "bitcoin")
    days = int(context.args[1]) if len(context.args) > 1 else 90

    try:
        df = get_ohlc(coin, days=days, interval="daily")
    except Exception as e:
        await update.message.reply_text(f"🚨 Erreur données de marché : {e}")
        return

    if df.empty or "close" not in df.columns:
        await update.message.reply_text("⚠️ Impossible de récupérer l'historique demandé.")
        return

    closes = df["close"].tolist()
    summary = summarize_trend(closes)

    await update.message.reply_text(
        f"📉 Résumé simplifié du graphique {coin} sur {days} jours :\n\n{summary}\n\n"
        "ℹ️ Résumé orienté lecture du graphique, pas de recommandation de trading."
    )
