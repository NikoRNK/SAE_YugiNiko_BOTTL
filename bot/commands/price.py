from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_price_usd, normalize_coin


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "📌 Usage :\n"
            "➡️ /price bitcoin\n"
            "➡️ /price eth"
        )
        return

    raw = context.args[0]
    coin_id = normalize_coin(raw)

    try:
        value = get_price_usd(coin_id)
        await update.message.reply_text(
            "💰 Prix actuel\n"
            f"🪙 Monnaie : {raw} (id : {coin_id})\n"
            f"📈 Valeur : {value:.4f} $"
        )

    except KeyError:
        await update.message.reply_text(
            "⚠️ Monnaie inconnue.\n"
            "Le bot utilise une API avec une liste précise de cryptos.\n"
            "Attention à bien écrire le nom de la monnaie (orthographe exacte), "
            "par exemple : bitcoin, ethereum, solana."
        )

    except Exception as e:
        await update.message.reply_text(
            f"🚨 Erreur technique pour {raw} : {e}"
        )
