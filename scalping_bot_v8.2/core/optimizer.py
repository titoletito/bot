# core/optimizer.py – Analyse complète avec résumé stratégique

import pandas as pd
import os

LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs', 'signals.csv'))
REPORT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports', 'filter_report.csv'))

os.makedirs('reports', exist_ok=True)

MIN_WINRATE = 0.4
MIN_SAMPLE = 10

def analyse_filters():
    if not os.path.exists(LOG_FILE):
        print("[OPTIMIZER] Aucun log trouvé.")
        return

    df = pd.read_csv(LOG_FILE)
    if df.empty:
        print("[OPTIMIZER] Log vide.")
        return

    filter_cols = [
        'ema_ok', 'squeeze_ok', 'breakout_ok', 'vwap_ok', 'volume_ok',
        'supertrend_ok', 'adx_ok', 'pattern_ok'
    ]

    report = []
    low_perf = []
    low_sample = []
    stable = []

    print("\n[OPTIMIZER] Analyse des filtres actifs :")
    for col in filter_cols:
        subset = df[df[col] == True]
        total = len(subset)
        if total < MIN_SAMPLE:
            print(f"[OPTIMIZER] {col:<15} → ! Échantillon insuffisant ({total})")
            low_sample.append(col)
            continue

        winrate = round((subset['pnl'] > 0).sum() / total * 100, 2)
        pnl_avg = round(subset['pnl'].mean(), 2)
        tag = "O OK" if winrate >= (MIN_WINRATE * 100) else "! Inefficace"
        print(f"{col:<15} → Winrate: {winrate:>5}% | PNL: {pnl_avg:>6} | Trades: {total:<3} → {tag}")

        report.append({
            'filtre': col,
            'trades': total,
            'winrate_%': winrate,
            'pnl_moyen': pnl_avg,
            'efficace': tag
        })

        if tag == "! Inefficace":
            low_perf.append(col)
        elif tag == "O OK":
            stable.append(col)

    pd.DataFrame(report).to_csv(REPORT_FILE, index=False)
    print(f"\n[OPTIMIZER] Rapport CSV enregistré : {REPORT_FILE}")

    # Résumé stratégique
    print("\n[OPTIMIZER] Résumé stratégique :")
    if low_perf:
        print(f"X À désactiver : {', '.join(low_perf)}")
    if low_sample:
        print(f"! À surveiller (échantillon faible) : {', '.join(low_sample)}")
    if stable:
        print(f"O Filtres solides : {', '.join(stable)}")

def analyse_scores(df):
    print("\n[OPTIMIZER] Analyse par score :")
    for score in sorted(df['score'].dropna().unique()):
        subset = df[df['score'] == score]
        total = len(subset)
        if total < MIN_SAMPLE:
            continue
        winrate = round((subset['pnl'] > 0).sum() / total * 100, 2)
        pnl_avg = round(subset['pnl'].mean(), 2)
        print(f"Score {score:<4} → Trades: {total:<3} | Winrate: {winrate:>5}% | PNL moyen: {pnl_avg}")


def analyse_sides(df):
    print("\n[OPTIMIZER] Analyse par direction (BUY/SELL) :")
    for side in ['BUY', 'SELL']:
        subset = df[df['side'] == side]
        total = len(subset)
        if total == 0:
            continue
        winrate = round((subset['pnl'] > 0).sum() / total * 100, 2)
        pnl_avg = round(subset['pnl'].mean(), 2)
        pnl_total = round(subset['pnl'].sum(), 2)
        print(f"{side:<5} → Trades: {total:<3} | Winrate: {winrate:>5}% | PNL moyen: {pnl_avg} | Total: {pnl_total}")


def analyse_outcomes(df):
    print("\n[OPTIMIZER] Répartition des issues :")
    for outcome, count in df['outcome'].value_counts().items():
        pct = round((count / len(df)) * 100, 1)
        print(f"{outcome:<10} : {count} trades ({pct}%)")

        
if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        print("[OPTIMIZER] Aucun log trouvé.")
        exit()

    df = pd.read_csv(LOG_FILE)
    if df.empty:
        print("[OPTIMIZER] Log vide.")
        exit()

    analyse_filters()
    analyse_scores(df)
    analyse_sides(df)
    analyse_outcomes(df)

