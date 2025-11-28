from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_price_usd, normalize_coin


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "<b>Usage :</b>\n"
            "/price bitcoin\n"
            "/price eth"
        )
        return

    raw = context.args[0]
    coin_id = normalize_coin(raw)

    try:
        value = get_price_usd(coin_id)
        await update.message.reply_text(
            f"<b>Prix actuel</b>\n"
            f"Monnaie : de>{raw}</code> (id : de>{coin_id}</code>)\n"
            f"Valeur : <b>{value:.4f} $</b>"
        )

    except KeyError:
        await update.message.reply_text(
            "<b>Monnaie inconnue.</b>\n"
            "Le bot utilise une API avec une liste précise de cryptos.\n"
            "Attention à bien écrire le nom de la monnaie (orthographe exacte), "
            "par exemple : de>bitcoin</code>, de>ethereum</code>, de>solana</code>."
        )

    except Exception as e:
        await update.message.reply_text(
            f"<b>Erreur technique</b> pour de>{raw}</code> : de>{e}</code>"
        )
