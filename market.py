# market.py
import requests
import pandas as pd
from datetime import datetime

def fetch_data_coingecko(coin_id="binancecoin", vs_currency="usd", days=1):
    """
    Obtiene datos históricos de CoinGecko.
    Se obtienen datos con intervalo 'hourly'.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": vs_currency, "days": days, "interval": "hourly"}
    response = requests.get(url, params=params)
    data = response.json()
    # data['prices'] contiene [timestamp, price]
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    # Simulamos las columnas OHLCV (para indicadores)
    df['open'] = df['price']
    df['high'] = df['price']
    df['low'] = df['price']
    df['close'] = df['price']
    df['volume'] = 1  # Valor dummy
    return df
