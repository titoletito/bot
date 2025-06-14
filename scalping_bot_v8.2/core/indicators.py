# core/indicators.py – Ajout des indicateurs techniques

import pandas as pd
import ta


def add_indicators(df):
    # EMA
    df['ema9'] = ta.trend.ema_indicator(df['close'], window=5)
    df['ema21'] = ta.trend.ema_indicator(df['close'], window=10)
    df['ema55'] = ta.trend.ema_indicator(df['close'], window=20)
    df['ema100'] = ta.trend.ema_indicator(df['close'], window=100)

    # RSI
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=7).rsi()

    # ATR
    df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=10).average_true_range()

    # VWAP (custom)
    df['vwap'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()
    # Filtre VWAP avec distance minimale (0.2%)
    df['vwap_distance'] = abs(df['close'] - df['vwap']) / df['vwap']
    df['vwap_ok'] = (df['close'] > df['vwap']) & (df['vwap_distance'] > 0.002)


    # Bollinger Bands & Keltner Channel pour squeeze
    bb = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
    kc = ta.volatility.KeltnerChannel(high=df['high'], low=df['low'], close=df['close'], window=20)
    df['bb_bwidth'] = bb.bollinger_hband() - bb.bollinger_lband()
    df['kc_width'] = kc.keltner_channel_hband() - kc.keltner_channel_lband()
    df['squeeze_on'] = df['bb_bwidth'] < (df['kc_width'] * 1.05)

    # Supertrend (10, 3.0)
    atr = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close'], window=7)
    hl2 = (df['high'] + df['low']) / 2
    upperband = hl2 + 2 * atr.average_true_range()
    lowerband = hl2 - 2 * atr.average_true_range()


    supertrend = [True]  # première valeur arbitraire

    for i in range(1, len(df)):
        if df['close'].iloc[i] > upperband.iloc[i - 1]:
            supertrend.append(True)
        elif df['close'].iloc[i] < lowerband.iloc[i - 1]:
            supertrend.append(False)
        else:
            supertrend.append(supertrend[-1])

    df['supertrend'] = supertrend

    # ADX
    df['adx'] = ta.trend.ADXIndicator(df['high'], df['low'], df['close'], window=10).adx()

    return df
