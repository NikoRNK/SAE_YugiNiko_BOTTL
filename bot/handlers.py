from telegram.ext import Application, CommandHandler

from .commands.start import start
from .commands.price import price
from .commands.prices import prices
from .commands.market import market
from .commands.volatility import volatility
from .commands.help import help_command

from .command_registry import register_command  # <<< nouveau


def add_command(app: Application, name: str, callback, description: str) -> None:
    app.add_handler(CommandHandler(name, callback))
    register_command(name, description)


def register_handlers(app: Application) -> None:
    add_command(app, "start", start, "Démarrer le bot et afficher l’accueil.")
    add_command(app, "help", help_command, "Afficher la liste des commandes.")
    add_command(app, "price", price, "Prix actuel d'une crypto.")
    add_command(app, "prices", prices, "Prix de plusieurs cryptos.")
    add_command(app, "market", market, "Vue marché (prix, Δ24h, volume).")
    add_command(app, "volatility", volatility, "Volatilité annualisée approximative.")
    # Tu rajoutes ici les futures commandes.
