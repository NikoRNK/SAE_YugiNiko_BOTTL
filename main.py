from telegram.ext import ApplicationBuilder

from bot.handlers import register_handlers

from bot.error_handler import error_handler

BOT_TOKEN = "8308086760:AAGiZMwR7Ea0HbwTpTkSY_gC9yyHcRCqxl4"


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(app)
    print("Bot lancé. Ctrl+C pour arrêter.")
    app.run_polling()


if __name__ == "__main__":
    main()

main.add_error_handler(error_handler)