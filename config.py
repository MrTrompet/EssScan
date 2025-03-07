# config.py

# Columnas para el modelo ML
feature_columns = ['open', 'high', 'low', 'close', 'volume', 'sma_long', 'bb_low', 'bb_medium', 'bb_high']

# Claves de API para pruebas (en producción usar variables de entorno)
API_KEY = 'TU_API_KEY'
API_SECRET = 'TU_API_KEY'

# Configuración de Telegram
TELEGRAM_TOKEN = 'TU_API_KEY'
# Usamos el chat id y thread id obtenidos:
TELEGRAM_CHAT_ID = 'TU_API_KEY'
TARGET_THREAD_ID = 2740  # ID del tema "Ecosystem Signals"

# Clave para OpenAI
OPENAI_API_KEY = 'TU_API_KEY'

# Otras configuraciones
SYMBOL = 'BNB/USDT'
TIMEFRAME = '4h'
MAX_RETRIES = 5
SCAN_INTERVAL = 5  # segundos entre cada escaneo
