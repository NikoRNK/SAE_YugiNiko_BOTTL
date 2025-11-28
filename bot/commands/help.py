from telegram import Update
from telegram.ext import ContextTypes


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Commandes dispo :\n"
        "/price in>\n"
        "/prices in1> in2>...\n"
        "/market [coin1 coin2]\n"
        "/chart in> <jours>\n"
        "/chart_ind in> <jours>\n"
        "/volatility in> <jours>"
    )
