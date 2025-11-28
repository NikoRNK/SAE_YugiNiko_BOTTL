from telegram.ext import ApplicationBuilder
from telegram.constants import ParseMode
from telegram.ext import Defaults

from bot.handlers import register_handlers

BOT_TOKEN = "8308086760:AAGiZMwR7Ea0HbwTpTkSY_gC9yyHcRCqxl4"


def main() -> None:
    defaults = Defaults(parse_mode=ParseMode.HTML)
    app = ApplicationBuilder().token(BOT_TOKEN).defaults(defaults).build()
    register_handlers(app)
    print("Bot lancé. Ctrl+C pour arrêter.")
    app.run_polling()


if __name__ == "__main__":
    main()
