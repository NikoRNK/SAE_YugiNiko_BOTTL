from telegram import Update
from telegram.ext import ContextTypes

from ..command_registry import COMMANDS_HELP


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lines = ["📚 Commandes disponibles :"]
    for cmd, desc in COMMANDS_HELP.items():
        lines.append(f"• {cmd} – {desc}")
    await update.message.reply_text("\n".join(lines))

async def boom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Je vais volontairement planter...")
    1 / 0  # division par zéro -> erreur