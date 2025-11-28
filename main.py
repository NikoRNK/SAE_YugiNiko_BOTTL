from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# ⚠️ Ton token en dur (pas conseillé en vrai, mais tu m'as dit que tu t'en fiches)
BOT_TOKEN = "8308086760:AAGiZMwR7Ea0HbwTpTkSY_gC9yyHcRCqxl4"

# Handler pour /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Salut {user.first_name}, je suis ton bot SAE (version init)."
    )

# Handler pour /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Commandes dispo pour l’instant :\n"
        "/start - dire bonjour\n"
        "/help  - afficher cette aide"
    )

def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot Telegram lancé (Ctrl+C pour arrêter)")
    app.run_polling()

if __name__ == "__main__":
    main()
