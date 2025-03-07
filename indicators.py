# indicators.py
import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
from ta.volatility import BollingerBands

def calculate_scan_indicators(data):
    """
    Calcula indicadores: SMA corta (window=10), SMA larga (window=25), RSI y Bandas de Bollinger.
    """
    data = data.copy()
    data['sma_short'] = SMAIndicator(data['close'], window=10).sma_indicator()
    data['sma_long'] = SMAIndicator(data['close'], window=25).sma_indicator()
    data['rsi'] = RSIIndicator(data['close'], window=14).rsi()
    bb = BollingerBands(data['close'], window=20, window_dev=2)
    data['bb_low'] = bb.bollinger_lband()
    data['bb_medium'] = bb.bollinger_mavg()
    data['bb_high'] = bb.bollinger_hband()
    return data

def detect_cross(data):
    """
    Detecta el cruce entre la SMA corta y la SMA larga.
    Retorna "golden" para golden cross, "death" para death cross o None si no hay cruce.
    """
    if len(data) < 2:
        return None
    prev = data.iloc[-2]
    current = data.iloc[-1]
    if prev['sma_short'] < prev['sma_long'] and current['sma_short'] >= current['sma_long']:
        return "golden"
    if prev['sma_short'] > prev['sma_long'] and current['sma_short'] <= current['sma_long']:
        return "death"
    return None
