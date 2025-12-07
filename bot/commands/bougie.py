from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_ohlc


def describe_candle(open_, high, low, close) -> str:
    body = abs(close - open_)
    range_ = high - low
    upper_wick = high - max(open_, close)
    lower_wick = min(open_, close) - low

    if range_ == 0:
        return "Doji parfait : aucune variation, forte indécision."

    body_ratio = body / range_
    upper_ratio = upper_wick / range_
    lower_ratio = lower_wick / range_

    bullish = close > open_
    bearish = close < open_

    if body_ratio < 0.1 and upper_ratio > 0.4 and lower_ratio > 0.4:
        return "Doji / spinning top : petite bougie avec longues mèches, forte indécision du marché."
    if body_ratio < 0.3 and lower_ratio > 0.5 and upper_ratio < 0.2 and bullish:
        return "Marteau haussier : longue mèche basse et clôture au-dessus de l'ouverture, possible retournement haussier."
    if body_ratio < 0.3 and upper_ratio > 0.5 and lower_ratio < 0.2 and bearish:
        return "Marteau inversé baissier : longue mèche haute et clôture sous l'ouverture, pression vendeuse possible."
    if body_ratio > 0.6 and bullish:
        return "Grande bougie haussière : acheteurs largement dominants pendant cette période."
    if body_ratio > 0.6 and bearish:
        return "Grande bougie baissière : vendeurs largement dominants pendant cette période."

    return "Bougie standard : combinaison modérée de corps et de mèches, pas de pattern fort mais donne le ton du mouvement."


async def bougie(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /bougie [coin] [intervalle] -> ex: /bougie bitcoin 1d
    coin = (context.args[0].lower() if context.args else "bitcoin")

    try:
        df = get_ohlc(coin, days=2, interval="1d")
    except Exception as e:
        await update.message.reply_text(f"🚨 Erreur données de marché : {e}")
        return

    if df.empty:
        await update.message.reply_text("⚠️ Impossible de récupérer la dernière bougie.")
        return

    last = df.iloc[-1]
    explanation = describe_candle(
        last["open"], last["high"], last["low"], last["close"]
    )

    direction = "haussière" if last["close"] > last["open"] else "baissière" if last["close"] < last["open"] else "neutre"

    await update.message.reply_text(
        f"🕯 Bougie du dernier intervalle pour {coin} :\n"
        f"- Ouverture : {last['open']:.2f}\n"
        f"- Plus haut : {last['high']:.2f}\n"
        f"- Plus bas  : {last['low']:.2f}\n"
        f"- Clôture   : {last['close']:.2f}\n"
        f"- Direction : {direction}\n\n"
        f"🤖 Interprétation : {explanation}\n"
        "ℹ️ Analyse descriptive uniquement, pas de conseil d’investissement."
    )
