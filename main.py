# main.py
import time
from config import SYMBOL, SCAN_INTERVAL, TELEGRAM_CHAT_ID, TARGET_THREAD_ID
from market import fetch_data_coingecko
from indicators import calculate_scan_indicators, detect_cross
from ml_model import train_ml_model, predict_cross_strength
from telegram_handler import send_telegram_message, analyze_signal_with_chatgpt
from PrintGraphic import send_scan_graph

def compose_scan_message(cross_type, indicators, ml_confidence):
    if cross_type == "golden":
        tipo = "Cruce Dorado (Golden Cross)"
        recomendacion = "Posible entrada LONG"
    elif cross_type == "death":
        tipo = "Cruce de la Muerte (Death Cross)"
        recomendacion = "Posible entrada SHORT"
    else:
        return None
    message = (
        f"〘 ESS SCAN 〙\n"
        f"Agente, se ha detectado un {tipo}.\n"
        f"Precio: ${indicators['close']:.2f}\n"
        f"RSI: {indicators['rsi']:.2f}\n"
        f"SMA Corta: {indicators['sma_short']:.2f} | SMA Larga: {indicators['sma_long']:.2f}\n"
        f"Bandas Bollinger: Low ${indicators['bb_low']:.2f}, Med ${indicators['bb_medium']:.2f}, High ${indicators['bb_high']:.2f}\n"
        f"Confianza ML: {ml_confidence*100:.1f}%\n"
        f"Recomendación: {recomendacion}\n"
        f"Utiliza discreción. ¡Suerte, Agente!"
    )
    return message

def main():
    # Entrenamiento inicial usando los datos de las últimas 24 horas
    data = fetch_data_coingecko(coin_id="binancecoin", vs_currency="usd", days=1)
    data = calculate_scan_indicators(data)
    train_ml_model(data)
    
    last_signal = None
    while True:
        try:
            data = fetch_data_coingecko(coin_id="binancecoin", vs_currency="usd", days=1)
            data = calculate_scan_indicators(data)
            cross = detect_cross(data)
            if cross:
                ml_conf = predict_cross_strength(data)
                last_row = data.iloc[-1]
                message = compose_scan_message(cross, last_row, ml_conf)
                # Complementa el mensaje con análisis de ChatGPT
                final_message = analyze_signal_with_chatgpt(message)
                # Envía el mensaje al chat del grupo, dirigido al thread TARGET_THREAD_ID
                send_telegram_message(final_message, chat_id=TELEGRAM_CHAT_ID, message_thread_id=TARGET_THREAD_ID)
                # Envía el gráfico de señal
                send_scan_graph(TELEGRAM_CHAT_ID, timeframe="1h", cross_type=cross)
                last_signal = cross
            time.sleep(SCAN_INTERVAL)
        except Exception as e:
            print(f"Error en el escaneo: {e}")
            time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()
