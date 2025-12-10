from telegram.ext import Application, CommandHandler

from .commands.start import start
from .commands.price import price
from .commands.prices import prices
from .commands.market import market
from .commands.volatility import volatility
from .commands.help import help_command, boom
from .commands.chart import chart
from .commands.chart_ind import chart_ind
from .commands.ia import ia
from .commands.ia import ia
from .commands.motscles import motscles
from .commands.tendance7 import tendance7
from .commands.bougie import bougie
from .commands.simplifie import simplifie


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
    add_command(app, "chart", chart, "Graphique des prix d'une crypto (ex. /chart bitcoin 7).")
    add_command(app, "chart_ind", chart_ind, "Graphique avec indicateurs techniques (ex. /chart_ind Bitcoin [finance:Bitcoin] 30).")
    add_command(app, "ia", ia, "Analyse IA du sentiment des news crypto sur 24h.")
    add_command(app, "ia", ia, "Analyse IA du sentiment des news sur 24h.")
    add_command(app, "motscles", motscles, "Mots-clés dominants dans les news crypto.")
    add_command(app, "tendance7", tendance7, "Tendance de prix sur 7 jours pour une crypto.")
    add_command(app, "bougie", bougie, "Explique la dernière bougie (bullish/bearish, marteau, doji...).")
    add_command(app, "simplifie", simplifie, "Résumé texte d'un graphique sur N jours.")
    add_command(app, "boom", boom, "Commande de test pour le error handler.")
    # Tu rajoutes ici les futures commandes.
