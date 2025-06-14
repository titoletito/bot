# signal_engine.py – avec filtres EMA100 (trend) et ATR (volatilité minimale)
import sys
import os
from datetime import datetime
from colorama import Fore, Style, init
init(autoreset=True)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

last_direction = None


def print_debug_signal(latest, score, filters):
    print(f"\n{Style.BRIGHT}[{latest.name}] 🧠 SIGNAL DEBUG{Style.RESET_ALL}")
    print(
        f"EMA: {latest['ema9']:.2f}/{latest['ema21']:.2f}/{latest['ema55']:.2f} "
        f"| EMA100: {latest['ema100']:.2f} "
        f"| RSI: {latest['rsi']:.2f} "
        f"| ATR: {latest['atr']:.2f} "
        f"| VWAP: {latest['vwap']:.2f} "
        f"| Volume: {int(latest['volume'])} "
        f"| Score: {score:.1f} (seuil: {config.SCORE_THRESHOLD})"
    )
    print(
        f"[FILTERS] EMA: {'✅' if filters.get('ema_ok') else '❌'} "
        f"| Squeeze: {'✅' if filters.get('squeeze_ok') else '❌'} "
        f"| Breakout: {'✅' if filters.get('breakout_ok') else '❌'} "
        f"| VWAP: {'✅' if filters.get('vwap_ok') else '❌'} "
        f"| Volume: {'✅' if filters.get('volume_ok') else '❌'} "
        f"| Supertrend: {'✅' if filters.get('supertrend_ok') else '❌'} "
        f"| ADX: {'✅' if filters.get('adx_ok') else '❌'} "
        f"| Pattern: {'✅' if filters.get('pattern_ok') else '❌'}"
    )


def generate_signal(df):
    latest = df.iloc[-1]
    previous = df.iloc[-2]
    score = 0
    direction = None
    global last_direction
    last_direction = direction
    filters = {}

    # EMA logic
    filters['ema_ok'] = bool(latest['ema9'] > latest['ema21'] > latest['ema55'] or latest['ema9'] < latest['ema21'] < latest['ema55'])
    if filters['ema_ok']:
        score += config.WEIGHTS['ema']
        direction = 'BUY' if latest['ema9'] > latest['ema21'] else 'SELL'
        

    # Tendance globale (EMA100)
    trend_ok = (
    (direction == 'BUY' and latest['close'] > latest['ema100'] and df['supertrend'].iloc[-1]) or
    (direction == 'SELL' and latest['close'] < latest['ema100'] and not df['supertrend'].iloc[-1])
)

    if not trend_ok:
        print("[FILTER] Bloqué par Supertrend ou EMA100 incohérent")
        print_debug_signal(latest, score, filters)
        return None, filters

    filters['supertrend_ok'] = True


    # Volatilité minimale (ATR)
    if latest['atr'] < 6:
        print("[FILTER] Bloqué par volatilité trop faible (ATR)")
        print_debug_signal(latest, score, filters)
        return None, filters

    filters['squeeze_ok'] = bool(latest['squeeze_on'])
    if filters['squeeze_ok']:
        score += config.WEIGHTS['squeeze']

    filters['breakout_ok'] = bool((direction == 'BUY' and latest['close'] > previous['high']) or
                                  (direction == 'SELL' and latest['close'] < previous['low']))
    if filters['breakout_ok']:
        score += config.WEIGHTS['breakout']

    filters['vwap_ok'] = bool((direction == 'BUY' and latest['close'] > latest['vwap']) or
                               (direction == 'SELL' and latest['close'] < latest['vwap']))
    if filters['vwap_ok']:
        score += config.WEIGHTS['vwap']

    volume_ma = df['volume'].rolling(window=20).mean().iloc[-1]
    filters['volume_ok'] = bool(latest['volume'] > 1.5 * volume_ma)
    if filters['volume_ok']:
        score += config.WEIGHTS['volume_spike']

    if latest['rsi'] > config.RSI_OVERBOUGHT or latest['rsi'] < config.RSI_OVERSOLD:
        if score >= config.SCORE_THRESHOLD and trend_ok:
            print(f"[⚠️ OVERRIDE RSI] RSI extrême ({latest['rsi']:.2f}) mais tendance OK et score {score:.1f} => signal autorisé")
        else:
            print("[FILTER] Bloqué par RSI extrême")
            print_debug_signal(latest, score, filters)
            return None, filters


    filters['adx_ok'] = bool(df['adx'].iloc[-1] >= 20)
    if not filters['adx_ok']:
        print("[FILTER] Bloqué par ADX < 20")
        print_debug_signal(latest, score, filters)
        return None, filters

    filters['pattern_ok'] = (
        (direction == 'BUY' and df.iloc[-1]['high'] > df.iloc[-2]['high'] and df.iloc[-1]['close'] > df.iloc[-1]['open']) or
        (direction == 'SELL' and df.iloc[-1]['low'] < df.iloc[-2]['low'] and df.iloc[-1]['close'] < df.iloc[-1]['open'])
    )

    if filters['pattern_ok']:
        score += 1


    # Génération dynamique du setup_type basé sur les filtres actifs
    setup_filters = ['ema_ok', 'adx_ok', 'supertrend_ok', 'volume_ok', 'pattern_ok', 'breakout_ok']
    setup_parts = [name.replace('_ok', '') for name in setup_filters if filters.get(name)]
    setup_type = "_".join(setup_parts) if setup_parts else "autre"



# Validation finale du signal
    if score >= config.SCORE_THRESHOLD and direction:
        print_debug_signal(latest, score, filters)
        return {
            'side': direction,
            'score': score,
            'setup_type': setup_type
        }, filters

    return None, filters
