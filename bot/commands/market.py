from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_market_snapshot


async def market(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    ids = [c.lower() for c in context.args] or ["bitcoin", "ethereum"]
    try:
        snap = get_market_snapshot(ids)
    except Exception as e:
        await update.message.reply_text(f"Erreur API : {e}")
        return
    lines = []
    for cid, info in snap["coins"].items():
        lines.append(
            f"{cid}: {info['price']:.2f} $ | Δ24h {info['change_24h']:.2f}% | Vol24h {info['volume_24h']:.0f}"
        )
    lines.append(f"Dominance BTC: {snap['btc_dominance']:.2f}%")
    await update.message.reply_text("\n".join(lines))
