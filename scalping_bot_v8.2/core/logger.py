# core/logger.py – Log enrichi avec détails des filtres + setup_type

import csv
import os
from datetime import datetime

LOG_FILE = 'logs/signals.csv'
os.makedirs('logs', exist_ok=True)

# Créer le fichier si inexistant avec en-tête enrichi
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'timestamp', 'side', 'score', 'setup_type', 'pnl', 'outcome', 'mode',
            'ema_ok', 'squeeze_ok', 'breakout_ok', 'vwap_ok', 'volume_ok',
            'supertrend_ok', 'adx_ok', 'pattern_ok'
        ])

def log_trade(df, signal, result, filters, mode='real'):
    timestamp = df.index[-1].strftime('%Y-%m-%d %H:%M:%S')
    row = [
        timestamp,
        result['side'],
        round(signal['score'], 2),
        signal.get('setup_type', 'na'),
        round(result['pnl'], 4),
        result['outcome'],
        mode,
        filters.get('ema_ok'),
        filters.get('squeeze_ok'),
        filters.get('breakout_ok'),
        filters.get('vwap_ok'),
        filters.get('volume_ok'),
        filters.get('supertrend_ok'),
        filters.get('adx_ok'),
        filters.get('pattern_ok')
    ]
    with open(LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)
