import sqlite3
import time
from config import COUNT, PER_HOUR, DB_PATH

def init_db():
    """Inicializa la base de datos y crea la tabla si no existe."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            count INTEGER DEFAULT 0,
            last_reset INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def can_process_voice(user_id):
    """Verifica si el usuario puede procesar otro mensaje de voz."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    current_time = int(time.time())
    one_hour = PER_HOUR
    
    cursor.execute("SELECT count, last_reset FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    if result:
        count, last_reset = result
        if current_time - last_reset > one_hour:
            cursor.execute("UPDATE users SET count = 1, last_reset = ? WHERE user_id = ?", (current_time, user_id))
            conn.commit()
            conn.close()
            return True
        elif count < COUNT:
            cursor.execute("UPDATE users SET count = count + 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            return False
    else:
        cursor.execute("INSERT INTO users (user_id, count, last_reset) VALUES (?, 1, ?)", (user_id, current_time))
        conn.commit()
        conn.close()
        return True
