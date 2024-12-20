from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import TOKEN
from handlers.commands import start, help_command
from handlers.voice import handle_voice, handle_buttons
from db import init_db

def main():
    """Función principal para ejecutar el bot."""
    # Inicializar la base de datos
    init_db()
    
    app = ApplicationBuilder().token(TOKEN).build()

    # Añadir comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Añadir manejadores de mensajes
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("Bot iniciando...")
    app.run_polling()

if __name__ == '__main__':
    main()