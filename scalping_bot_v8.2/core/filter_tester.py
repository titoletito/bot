# core/filter_tester.py – Boucle de test automatique des filtres

import os
import subprocess
import pandas as pd
import time

FILTERS_TO_TEST = [
    'breakout_ok',
    'vwap_ok',
    'volume_ok',
    'supertrend_ok',
    'adx_ok',
    'pattern_ok',
    'squeeze_ok'
]

BASE_CONFIG_PATH = '../config.py'
BACKUP_PATH = '../config_backup.py'

LOG_FILE = '../logs/signals.csv'
REPORT = []

def update_filter_config(active_filter):
    with open(BASE_CONFIG_PATH, 'r') as f:
        lines = f.readlines()

    with open(BASE_CONFIG_PATH, 'w') as f:
        for line in lines:
            if line.strip().startswith('FILTERS ='):
                f.write(f"FILTERS = ['ema_ok', '{active_filter}']\n")
            else:
                f.write(line)

def run_main():
    subprocess.run(['python', 'C:/Users/Ophélie/Desktop/scalping_bot_v8/main.py'])

def analyze_results(active_filter):
    df = pd.read_csv(LOG_FILE)
    df = df[df['side'].notna()]  # éviter les signaux bloqués
    trades = len(df)
    pnl = round(df['pnl'].sum(), 2)
    winrate = round((df['pnl'] > 0).sum() / trades * 100, 2) if trades else 0
    REPORT.append([active_filter, trades, winrate, pnl])

def restore_config():
    if os.path.exists(BACKUP_PATH):
        with open(BACKUP_PATH, 'r') as f:
            content = f.read()
        with open(BASE_CONFIG_PATH, 'w') as f:
            f.write(content)

def backup_config():
    with open(BASE_CONFIG_PATH, 'r') as f:
        content = f.read()
    with open(BACKUP_PATH, 'w') as f:
        f.write(content)

def main():
    backup_config()

    for f in FILTERS_TO_TEST:
        print(f"[TEST] Filtre: {f}")
        update_filter_config(f)
        run_main()
        analyze_results(f)
        time.sleep(1)

    restore_config()

    print("\n✅ Résultats :")
    df_report = pd.DataFrame(REPORT, columns=['Filtre', 'Trades', 'Winrate %', 'PNL total'])
    print(df_report.to_string(index=False))

if __name__ == '__main__':
    main()
