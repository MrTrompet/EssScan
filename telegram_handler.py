# telegram_handler.py
import requests
import openai
import time
from langdetect import detect
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, OPENAI_API_KEY, SYMBOL, TIMEFRAME, TARGET_THREAD_ID
from market import fetch_data_coingecko
from indicators import calculate_scan_indicators

openai.api_key = OPENAI_API_KEY
START_TIME = int(time.time())

def send_telegram_message(message, chat_id=None, message_thread_id=None):
    """Envía un mensaje a Telegram, incluyendo message_thread_id si se proporciona."""
    if not chat_id:
        chat_id = TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    if message_thread_id:
        payload['message_thread_id'] = message_thread_id
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Error al enviar mensaje a Telegram: {response.text}")
    except Exception as e:
        print(f"Error en la conexión con Telegram: {e}")

def analyze_signal_with_chatgpt(message):
    """
    Envía el mensaje a la API de OpenAI para obtener un análisis contextual.
    """
    system_prompt = (
        "Eres Higgs X, el agente de inteligencia encargado de vigilar el ecosistema. "
        "Responde de forma concisa y con un toque misterioso."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=150,
            temperature=0.7
        )
        answer = response.choices[0].message.content.strip()
        return answer
    except Exception as e:
        return f"⚠️ Error en análisis AI: {e}"

def get_updates():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            updates = response.json().get("result", [])
            return [upd for upd in updates if upd.get("message", {}).get("date", 0) >= START_TIME]
        else:
            print(f"Error al obtener actualizaciones: {response.text}")
            return []
    except Exception as e:
        print(f"Error en la conexión con Telegram: {e}")
        return []
