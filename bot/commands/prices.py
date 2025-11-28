from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_multi_prices_usd


async def prices(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "📊 Usage :\n"
            "➡️ /prices bitcoin ethereum solana"
        )
        return

    ids = [c.lower() for c in context.args]

    try:
        data = get_multi_prices_usd(ids)
    except Exception as e:
        await update.message.reply_text(f"🚨 Erreur API : {e}")
        return

    if not data:
        await update.message.reply_text("⚠️ Aucun prix trouvé pour les cryptos demandées.")
        return

    # Construire les lignes dans le même ordre que la saisie
    lines = [
        f"🪙 {cid} : {data[cid]:.4f} $"
        for cid in ids
        if cid in data
    ]

    await update.message.reply_text("💰 Prix actuels :\n" + "\n".join(lines))
