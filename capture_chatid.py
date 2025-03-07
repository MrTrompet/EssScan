# capture_chatid.py
import requests
import time

# Configura tu token
TELEGRAM_TOKEN = '7768315391:AAGWcnyjHqtxNrYmlAGHUzUa7F9Y85-lc94'

def get_updates():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("result", [])
        else:
            print(f"Error al obtener actualizaciones: {response.text}")
            return []
    except Exception as e:
        print(f"Error en la conexión: {e}")
        return []

def capture_chat_ids():
    print("Esperando actualizaciones... Envía un mensaje en el grupo/tema de interés.")
    while True:
        updates = get_updates()
        if updates:
            for upd in updates:
                message = upd.get("message", {})
                chat = message.get("chat", {})
                chat_id = chat.get("id")
                thread_id = message.get("message_thread_id")
                print("Chat ID:", chat_id)
                if thread_id:
                    print("Message Thread ID:", thread_id)
                else:
                    print("No se encontró Message Thread ID en este mensaje.")
            break
        time.sleep(3)

if __name__ == "__main__":
    capture_chat_ids()
