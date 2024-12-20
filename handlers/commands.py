from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja el comando /start."""
    await update.message.reply_text("¡Hola! Soy tu bot de Telegram. Usa /help para más información.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja el comando /help."""
    await update.message.reply_text("Comandos disponibles:\n/start - Iniciar el bot\n/help - Mostrar ayuda\n Enviame un mensaje de voz para transcribir o traducir de español a inglés.")
