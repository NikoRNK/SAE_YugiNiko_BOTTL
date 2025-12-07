import re
from collections import Counter
from telegram import Update
from telegram.ext import ContextTypes

from .ia import fetch_crypto_headlines  # on réutilise ta fonction


STOPWORDS = {
    "the","a","an","of","for","and","or","to","in","on","with","by","from","at",
    "le","la","les","un","une","des","de","du","au","aux","et","ou","dans","sur",
    "pour","par","en","est","être","ce","ces","cette","plus","moins","new","news",
    "crypto","cryptocurrency","bitcoin","btc","ethereum","eth"
}


def extract_keywords(titles: list[str], top_k: int = 10) -> list[tuple[str,int]]:
    words: list[str] = []
    for t in titles:
        for w in re.findall(r"\b\w+\b", t.lower()):
            if w.isdigit():
                continue
            if w in STOPWORDS:
                continue
            words.append(w)
    counts = Counter(words)
    return counts.most_common(top_k)


async def motscles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("🔍 Analyse des mots-clés dans les news...")

    titles, error = fetch_crypto_headlines(limit=50)
    if error:
        await update.message.reply_text(error)
        return

    top = extract_keywords(titles, top_k=10)
    if not top:
        await update.message.reply_text("⚠️ Impossible d'extraire des mots-clés.")
        return

    lines = ["🧠 Mots-clés dominants dans les news récentes :"]
    for word, count in top:
        lines.append(f"• {word} ({count} occurrences)")

    await update.message.reply_text("\n".join(lines))
