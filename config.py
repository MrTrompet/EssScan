# config.py

# Columnas para el modelo ML
feature_columns = ['open', 'high', 'low', 'close', 'volume', 'sma_long', 'bb_low', 'bb_medium', 'bb_high']

# Configuración de Telegram
import os

API_KEY = os.getenv('API_KEY', 'default_api_key')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TARGET_THREAD_ID = int(os.getenv('TARGET_THREAD_ID', 2740))  # ID del tema "Ecosystem Signals"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Otras configuraciones
SYMBOL = 'BNB/USDT'
TIMEFRAME = '4h'
MAX_RETRIES = 5
SCAN_INTERVAL = 5  # segundos entre cada escaneo
