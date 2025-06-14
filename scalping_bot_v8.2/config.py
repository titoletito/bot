# config.py – Paramètres globaux

# Paramètres de base
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1m'
CAPITAL = 1000  # capital fictif pour paper trading

# Seuils
SCORE_THRESHOLD = 3
RSI_OVERBOUGHT = 80
RSI_OVERSOLD = 20

# Sessions horaires (UTC)
TRADING_HOUR_START = '07:00'
TRADING_HOUR_END = '20:00'

# Logging
LOG_PATH = 'logs/signals.csv'

# Pondérations des signaux
WEIGHTS = {
    'ema': 1.0,           # très fiable comme filtre de tendance
    'breakout': 1.0,      # excellent sur BTC/USDT en M1
    'vwap': 1.0,          # bon filtre de confluence
    'volume_spike': 1.0,  # confirme les breakout forts
    'supertrend': 1.0,    # filtre de direction utile mais bruité
    'adx': 1.0,           # bon filtre pour momentum
    'pattern': 1.0,       # utile mais pas seul
    'squeeze': 1.0        # très bruité seul, utile combiné
}


DISABLE_HOUR_FILTER = True  # TEMP

