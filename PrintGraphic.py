# PrintGraphic.py
import pandas as pd
import io
import requests
import mplfinance as mpf
from config import SYMBOL, TELEGRAM_TOKEN

def send_scan_graph(chat_id, timeframe="1h", cross_type="golden"):
    """
    Genera un gráfico de velas con SMA y líneas de soporte/resistencia,
    y lo envía a Telegram. Se personaliza según el tipo de cruce.
    """
    # Para el ejemplo, generamos datos simulados
    import matplotlib.pyplot as plt
    import numpy as np
    dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='H')
    data = pd.DataFrame({
        'open': np.random.uniform(300,400, size=100),
        'high': np.random.uniform(400,500, size=100),
        'low': np.random.uniform(200,300, size=100),
        'close': np.random.uniform(300,400, size=100),
        'volume': np.random.uniform(100,1000, size=100)
    }, index=dates)
    
    sma_short = data['close'].rolling(window=10).mean()
    sma_long = data['close'].rolling(window=25).mean()
    support = data['close'].min()
    resistance = data['close'].max()
    
    buf = io.BytesIO()
    caption = f"{SYMBOL} - {timeframe} - {cross_type.capitalize()} Cross"
    
    mc = mpf.make_marketcolors(up='green', down='red', inherit=True)
    style = mpf.make_mpf_style(marketcolors=mc, gridstyle="--", facecolor='black', edgecolor='white', gridcolor='white')
    ap0 = mpf.make_addplot(sma_short, color='cyan')
    ap1 = mpf.make_addplot(sma_long, color='magenta')
    sr_support = [support] * len(data)
    sr_resistance = [resistance] * len(data)
    ap2 = mpf.make_addplot(sr_support, color='green', linestyle='--', width=0.8)
    ap3 = mpf.make_addplot(sr_resistance, color='red', linestyle='--', width=0.8)
    
    fig, axlist = mpf.plot(
        data,
        type='candle',
        style=style,
        title=caption,
        volume=False,
        addplot=[ap0, ap1, ap2, ap3],
        returnfig=True
    )
    fig.savefig(buf, dpi=100, format='png')
    plt.close(fig)
    buf.seek(0)
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    files = {'photo': buf}
    payload = {'chat_id': chat_id, 'caption': caption, 'message_thread_id': 2740}
    response = requests.post(url, data=payload, files=files)
    if response.status_code != 200:
        print(f"Error al enviar el gráfico: {response.text}")
