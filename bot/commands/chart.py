from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from ..services import get_ohlc


import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates


def build_price_chart_png(ohlc, file_path):
    """
    ohlc : liste de [timestamp_ms, open, high, low, close]
    file_path : objet Path ou str vers le fichier PNG à créer
    """
    # Met les données dans un DataFrame
    df = pd.DataFrame(ohlc, columns=["ts", "open", "high", "low", "close"])

    # Convertit les timestamps (en millisecondes) en datetime
    df["time"] = pd.to_datetime(df["ts"], unit="ms")

    fig, ax = plt.subplots(figsize=(8, 3))

    ax.plot(df["time"], df["close"], linewidth=1.5)

    ax.set_title("Prix en USD")
    ax.set_xlabel("Date")
    ax.set_ylabel("Prix")

    # Formattage propre des dates sur l'axe X
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    fig.autofmt_xdate()      # incline les labels de dates
    fig.tight_layout()

    fig.savefig(file_path, bbox_inches="tight")
    plt.close(fig)



async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /chart in> <jours>
    if len(context.args) < 2:
        await update.message.reply_text(
            "📊 Usage :\n"
            "➡️ /chart bitcoin 7"
        )
        return

    coin_id = context.args[0].lower()
    days_str = context.args[1]

    # Vérifier que le nombre de jours est un entier
    try:
        days = int(days_str)
    except ValueError:
        await update.message.reply_text(
            f"⚠️ Nombre de jours invalide : {days_str}\n"
            "Exemple : /chart bitcoin 7"
        )
        return

    # Récupérer les données OHLC
    try:
        ohlc = get_ohlc(coin_id, days)
    except Exception as e:
        await update.message.reply_text(f"🚨 Erreur API pour {coin_id} : {e}")
        return

    if not ohlc:
        await update.message.reply_text(
            f"⚠️ Impossible de récupérer les données pour {coin_id}."
        )
        return

    # Construire le graphique et l'envoyer
    file_path = Path("chart_price.png")
    build_price_chart_png(ohlc, file_path)

    await update.message.reply_photo(
        photo=open(file_path, "rb"),
        caption=f"📈 Graphique des prix sur {days} jours pour {coin_id}"
    )
