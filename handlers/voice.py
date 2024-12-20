# handlers/voice.py

import os
import tempfile
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from utils.helpers import transcribe_audio, handle_translation_voice, handle_translation_text, clean_temp_file
from db import can_process_voice

# Almacenar temporalmente la ruta del archivo
TEMP_FILE_PATH = None

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja mensajes de voz y ofrece opciones al usuario."""
    global TEMP_FILE_PATH

    # Descargar el archivo de voz
    file = await update.message.voice.get_file()
    tmp_dir = tempfile.mkdtemp()
    TEMP_FILE_PATH = os.path.join(tmp_dir, "voice_message.ogg")
    await file.download_to_drive(TEMP_FILE_PATH)

    await update.message.reply_text("¡Mensaje de voz recibido!")

    # Enviar botones de opciones
    reply_keyboard = [["Transcribir a inglés", "Traducir a inglés"]]
    await update.message.reply_text(
        "¿Qué quieres hacer con el mensaje?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja las acciones según la opción seleccionada."""
    global TEMP_FILE_PATH
    user_choice = update.message.text

    if TEMP_FILE_PATH and os.path.exists(TEMP_FILE_PATH):
        try:
            transcription = transcribe_audio(TEMP_FILE_PATH)
            
        except Exception as e:
            await update.message.reply_text(f"Error al transcribir el audio: {e}")
            return

        if user_choice == "Transcribir a inglés":
            await handle_translation_text(update, transcription)
            clean_temp_file(TEMP_FILE_PATH)
        elif user_choice == "Traducir a inglés":
            user_id = update.effective_user.id
            if not can_process_voice(user_id):
                await update.message.reply_text("Has alcanzado el límite de 5 mensajes de voz por hora. Intenta más tarde.")
                return
    
            await handle_translation_voice(update, transcription, TEMP_FILE_PATH, user_id)
    else:
        await update.message.reply_text("No hay ningún mensaje guardado.")

    await update.message.reply_text("Acción completada.", reply_markup=ReplyKeyboardRemove())
