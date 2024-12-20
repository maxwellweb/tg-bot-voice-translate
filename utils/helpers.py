import os
import errno
import whisper
from translate import Translator
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from config import ELEVENLABS_API_KEY

def transcribe_audio(file_path):
    """Transcribe el audio usando Whisper."""
    model = whisper.load_model("base")
    result = model.transcribe(file_path, fp16=False)
    return result["text"]

async def handle_translation_text(update, transcription):
    try:
        translator = Translator(from_lang="es", to_lang="en")
        translated_text = translator.translate(transcription)
    except Exception as e: 
        await update.message.reply_text(f"Algo salio mal con la traduccion: {e}")
    
    await update.message.reply_text(translated_text)
    
async def handle_translation_voice(update, transcription, file_path, user_id):
    """Traduce el texto al inglés y envía el audio generado."""
    try:
        translator = Translator(from_lang="es", to_lang="en")
        translated_text = translator.translate(transcription)
    except Exception as e:
        await update.message.reply_text(f"Error en la traducción: {e}")
        return

    # Generar el audio usando ElevenLabs
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    response = client.text_to_speech.convert(
        voice_id="pNInz6obpgDQGcFmaJgB",  # Voz de ejemplo (Adam)
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=translated_text,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.75,
            similarity_boost=0.5,
            style=0.0,
            use_speaker_boost=True,
        ),
    )
    message_id = update.effective_message.id

    save_file_path = f"voices/{user_id}/{message_id}_voice_message_translate.ogg"
    if not os.path.exists(os.path.dirname(save_file_path)):
        try:
            os.makedirs(os.path.dirname(save_file_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    await update.message.reply_audio(audio=open(save_file_path, 'rb'))
    clean_temp_file(file_path)

def clean_temp_file(file_path):
    """Elimina el archivo temporal."""
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
