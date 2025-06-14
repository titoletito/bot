# execution.py – version réaliste (TP/SL simulés sans fuite)
def execute_trade(df, signal, capital, risk_per_trade=0.01, max_duration=None):
    entry_index = df.index[-1]
    entry_price = df.iloc[-1]['close']
    atr = df.iloc[-1]['atr']
    volatility_phase = 'high' if atr > 20 else 'normal'
    if max_duration is None:
        max_duration = 40 if volatility_phase == 'high' else 30

    if volatility_phase == 'high':
        sl_distance = atr * 1.5
        tp_distance = atr * 2.5
    else:
        sl_distance = atr
        tp_distance = atr * 1.5

    if signal['side'] == 'BUY':
        stop_loss = entry_price - sl_distance
        take_profit = entry_price + tp_distance
    else:
        stop_loss = entry_price + sl_distance
        take_profit = entry_price - tp_distance

    outcome = 'TIMEOUT'
    exit_price = entry_price  # fallback par défaut

    for i in range(1, max_duration + 1):
        if len(df) < i + 1:
            break  # pas assez de données pour simuler

        row = df.iloc[-1 + i]

        if signal['side'] == 'BUY':
            if row['low'] <= stop_loss:
                exit_price = stop_loss
                outcome = 'SL'
                break
            elif row['high'] >= take_profit:
                exit_price = take_profit
                outcome = 'TP'
                break
        else:
            if row['high'] >= stop_loss:
                exit_price = stop_loss
                outcome = 'SL'
                break
            elif row['low'] <= take_profit:
                exit_price = take_profit
                outcome = 'TP'
                break

    if outcome == 'TIMEOUT':
        exit_price = df.iloc[-1 + max_duration]['close'] if len(df) > max_duration else df.iloc[-1]['close']

    if signal['side'] == 'BUY':
        pnl = exit_price - entry_price
    else:
        pnl = entry_price - exit_price

    return {
        'entry_time': entry_index,
        'entry': entry_price,
        'exit': exit_price,
        'side': signal['side'],
        'pnl': pnl,
        'outcome': outcome
    }
