import os
import requests
from telegram import Update
from telegram.ext import ContextTypes

from ..services import crypto_sentiment  # CryptoBERT


CRYPTOPANIC_TOKEN = "ee58dfaecb82cee305737495a2fdf074dfaae70d"
CRYPTOPANIC_URL = "https://cryptopanic.com/api/v1/posts/"


def fetch_crypto_headlines(limit: int = 20) -> tuple[list[str], str | None]:
    """Récupère quelques titres de news crypto récentes via CryptoPanic."""
    if not CRYPTOPANIC_TOKEN:
        return [], "⚠️ Variable d'environnement CRYPTOPANIC_TOKEN manquante."

    try:
        r = requests.get(
            CRYPTOPANIC_URL,
            params={"auth_token": CRYPTOPANIC_TOKEN, "kind": "news"},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        titles = [post["title"] for post in data.get("results", [])[:limit]]
        if not titles:
            return [], "⚠️ Aucune news crypto récente trouvée."
        return titles, None
    except Exception as e:
        return [], f"🚨 Erreur lors de la récupération des news : {e}"


async def ia(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Analyse le sentiment global du marché sur 24h à partir des news."""
    await update.message.reply_text("🤖 Analyse du sentiment des 24h en cours...")

    titles, error = fetch_crypto_headlines(limit=20)
    if error:
        await update.message.reply_text(error)
        return

    # 1) Analyse de sentiment avec CryptoBERT
    results = crypto_sentiment(titles)
    # results ~ [{'label': 'LABEL_1', 'score': 0.96}, ...]

    positives = sum(1 for r in results if r["label"] == "LABEL_1")
    negatives = sum(1 for r in results if r["label"] == "LABEL_0")
    total = len(results)
    pos_ratio = positives / total * 100

    if pos_ratio >= 60:
        overall = "😺 Sentiment global plutôt bullish sur les dernières 24h."
    elif pos_ratio <= 40:
        overall = "🐻 Sentiment global plutôt bearish sur les dernières 24h."
    else:
        overall = "😐 Sentiment global plutôt neutre / partagé sur les dernières 24h."

    lines: list[str] = [
        "🤖 Synthèse IA des news crypto (≈24h) :",
        overall,
        "",
        f"🟢 News positives : {positives}",
        f"🔴 News négatives : {negatives}",
        f"📊 Total news analysées : {total}",
        "",
        "📰 Exemples de titres analysés :",
    ]

    # 2) Afficher quelques titres avec leur couleur
    for title, r in list(zip(titles, results))[:5]:
        emoji = "🟢" if r["label"] == "LABEL_1" else "🔴"
        lines.append(f"{emoji} {title}")

    await update.message.reply_text("\n".join(lines))
