# core/fetch.py – Récupération des données OHLCV depuis Binance

import ccxt
import pandas as pd
import time

exchange = ccxt.binance({
    'enableRateLimit': True
})


def get_ohlcv(symbol='BTC/USDT', timeframe='1m', limit=200):
    try:
        data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"[ERREUR FETCH] {e}")
        return None
