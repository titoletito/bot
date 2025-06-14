# core/analyzer.py – Analyse quotidienne des performances

import pandas as pd
import os
from datetime import datetime

LOG_FILE = 'logs/signals.csv'
REPORT_FILE = 'reports/summary.csv'
os.makedirs('reports', exist_ok=True)


def generate_daily_summary():
    if not os.path.exists(LOG_FILE):
        print("[ANALYSE] Aucun log trouvé.")
        return

    df = pd.read_csv(LOG_FILE)
    if df.empty:
        print("[ANALYSE] Log vide.")
        return

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    today = datetime.utcnow().date()
    today_trades = df[df['timestamp'].dt.date == today]

    if today_trades.empty:
        print("[ANALYSE] Aucun trade pour aujourd'hui.")
        return

    total = len(today_trades)
    win_count = (today_trades['pnl'] > 0).sum()
    winrate = round((win_count / total) * 100, 2)
    avg_score = round(today_trades['score'].mean(), 2)
    pnl_total = round(today_trades['pnl'].sum(), 2)

    summary = pd.DataFrame([{
        'date': today.strftime('%Y-%m-%d'),
        'trades': total,
        'winrate_%': winrate,
        'avg_score': avg_score,
        'pnl_total': pnl_total
    }])

    if os.path.exists(REPORT_FILE):
        old = pd.read_csv(REPORT_FILE)
        summary = pd.concat([old, summary], ignore_index=True)

    summary.to_csv(REPORT_FILE, index=False)
    print(f"[ANALYSE] Résumé sauvegardé dans {REPORT_FILE}")
