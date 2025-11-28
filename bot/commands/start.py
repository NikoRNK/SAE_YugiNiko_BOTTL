from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Salut {user.first_name} !\n"
        "Je suis ton bot SAE crypto 🤖💰\n"
        "Tu peux par exemple essayer :\n"
        "• /price bitcoin\n"
        "• /prices bitcoin ethereum\n"
        "• /volatility bitcoin 30"
    )
