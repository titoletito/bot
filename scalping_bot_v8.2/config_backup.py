# config.py – Paramètres globaux

# Paramètres de base
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1m'
CAPITAL = 1000  # capital fictif pour paper trading

# Seuils
SCORE_THRESHOLD = 7
RSI_OVERBOUGHT = 75
RSI_OVERSOLD = 25

# Sessions horaires (UTC)
TRADING_HOUR_START = '07:00'
TRADING_HOUR_END = '18:00'

# Logging
LOG_PATH = 'logs/signals.csv'

# Pondérations des signaux
WEIGHTS = {
    'ema': 2.5,
    'squeeze': 0.5,
    'breakout': 2.5,
    'vwap': 1.5,
    'volume_spike': 2
}

DISABLE_HOUR_FILTER = False  # TEMP

