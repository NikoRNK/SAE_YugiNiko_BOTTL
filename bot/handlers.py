from telegram.ext import Application, CommandHandler

from .commands.start import start
from .commands.help import help_command
from .commands.price import price
from .commands.prices import prices
from .commands.market import market
from .commands.chart import chart
from .commands.chart_ind import chart_ind
from .commands.volatility import volatility


def register_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("prices", prices))
    app.add_handler(CommandHandler("market", market))
    app.add_handler(CommandHandler("chart", chart))
    app.add_handler(CommandHandler("chart_ind", chart_ind))
    app.add_handler(CommandHandler("volatility", volatility))
