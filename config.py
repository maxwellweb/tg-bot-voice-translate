# config.py

import logging
from dotenv import dotenv_values

# Cargar variables de entorno
config = dotenv_values(".env")

# Configuraciones globales
TOKEN = config["TG_TOKEN"]
ELEVENLABS_API_KEY = config["ELEVENLABS_API_KEY"]
COUNT = config["COUNT"]
PER_HOUR = config["PER_HOUR"]
DB_PATH = config["DB_PATH"]

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)