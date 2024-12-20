# Bot de Traducción de Voz para Telegram

Este proyecto es un bot de Telegram que permite a los usuarios enviar mensajes de voz y ofrece opciones para transcribir y traducir el mensaje a inglés. Además, el bot limita a los usuarios a **5 mensajes de voz por hora** usando una base de datos SQLite para el control de usuarios.

## Características

- **Transcribir mensajes de voz** en español a texto.
- **Traducir el texto transcrito** al inglés.
- **Generar audio traducido** usando ElevenLabs.
- **Límite de 5 mensajes de voz por hora** por usuario.
- **Base de datos SQLite** para almacenar usuarios y conteos de mensajes.

## Requisitos Previos

- **Python 3.8 o superior**.
- Un **bot de Telegram** creado con BotFather.
- Una **API Key de ElevenLabs** para síntesis de voz.
- Crea un fichero **voices** para almacenar las traducciones de voz.

## Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone https://github.com/maxwellweb/tg-bot-voice-translate.git
   cd tg-bot-voice-translate

    python3 -m venv .venv
    source .venv/bin/activate   # En macOS y Linux
    .\venv\Scripts\activate     # En Windows

    pip install -r requirements.txt

2. **Configura tu .env**
    TG_TOKEN=tu_token_de_telegram
    ELEVENLABS_API_KEY=tu_api_key_de_elevenlabs

3. **Iniciar el bot**
    ```bash 
        python main.py