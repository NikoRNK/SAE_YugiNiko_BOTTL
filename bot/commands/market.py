from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_market_snapshot


async def market(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Si l'utilisateur ne précise rien, on prend bitcoin et ethereum par défaut
    ids = [c.lower() for c in context.args] or ["bitcoin", "ethereum"]

    try:
        snap = get_market_snapshot(ids)
    except Exception as e:
        await update.message.reply_text(f"🚨 Erreur API : {e}")
        return

    if not snap or "coins" not in snap or not snap["coins"]:
        await update.message.reply_text("⚠️ Aucune donnée de marché trouvée pour les cryptos demandées.")
        return

    lines: list[str] = []
    for cid, info in snap["coins"].items():
        price = info["price"]
        change = info["change_24h"]
        vol = info["volume_24h"]
        lines.append(
            f"🪙 {cid} : {price:.2f} $ | 📊 Δ24h {change:.2f}% | 💸 Vol24h {vol:.0f}"
        )

    btc_dom = snap.get("btc_dominance")
    if btc_dom is not None:
        lines.append(f"🧱 Dominance BTC : {btc_dom:.2f}%")

    await update.message.reply_text("📈 Vue marché :\n" + "\n".join(lines))
