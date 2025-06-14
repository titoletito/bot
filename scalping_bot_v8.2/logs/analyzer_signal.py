import pandas as pd

# Charger le fichier CSV des signaux
df = pd.read_csv("signals.csv")

# Filtrer les trades réels uniquement (tu peux mettre "sim" si tu veux analyser les simulations)
df = df[df["mode"] == "real"]

results = []

for setup in df['setup_type'].unique():
    subset = df[df['setup_type'] == setup]
    total_trades = len(subset)
    win_trades = len(subset[subset['pnl'] > 0])
    pnl_total = subset['pnl'].sum()
    pnl_avg = subset['pnl'].mean()

    results.append({
        'setup_type': setup,
        'trades': total_trades,
        'wins': win_trades,
        'winrate': round(win_trades / total_trades * 100, 2) if total_trades else 0,
        'pnl_total': round(pnl_total, 2),
        'pnl_avg': round(pnl_avg, 4)
    })

results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by='pnl_total', ascending=False)

print(results_df.to_string(index=False))
