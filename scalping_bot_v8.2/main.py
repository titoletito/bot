# main.py – Phase complète avec filtres détaillés
from core import fetch, indicators, logger, signal_engine, execution, scheduler
import config
import time

capital = config.CAPITAL

print("[BOT] Lancement du scalping bot en mode paper trading réel...")

while True:
    if not scheduler.is_in_trading_hours():
        print("[INFO] Hors session de trading, en pause.")
        time.sleep(60)
        continue

    df = fetch.get_ohlcv(config.SYMBOL, config.TIMEFRAME)
    if df is None or len(df) < 100:
        print("[WARN] Pas assez de données pour analyser.")
        time.sleep(60)
        continue

    df = indicators.add_indicators(df)
    signal, filters = signal_engine.generate_signal(df)

    if signal:
        print(f"[SIGNAL] {signal['side']} détecté avec score {signal['score']:.2f}")
        result = execution.execute_trade(df, signal, capital)
        print(f"[TRADE] {result['side']} | Entrée: {result['entry']:.2f} | Sortie: {result['exit']:.2f} | PNL: {result['pnl']:.2f} | Résultat: {result['outcome']}")
        logger.log_trade(df, signal, result, filters, mode='real')

    else:
        from core import signal_engine  # pour accéder à last_direction

    if signal_engine.last_direction:
        debug_signal = {
            'side': signal_engine.last_direction,
            'score': 0,
            'setup_type': 'blocked_sim'
        }

        result = execution.execute_trade(df, debug_signal, capital)
        print(f"[DEBUG-SIM] {debug_signal['side']} | PNL: {result['pnl']:.2f} | Résultat: {result['outcome']}")
        logger.log_trade(df, debug_signal, result, filters, mode='sim')
 


    time.sleep(60)

