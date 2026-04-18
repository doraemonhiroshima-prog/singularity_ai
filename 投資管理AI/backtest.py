import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.rcParams["font.family"] = "MS Gothic"

# ===== 設定 =====
TICKERS = ["7203.T","6758.T","9984.T","6861.T","8035.T","9432.T","8306.T","4063.T","7974.T","6501.T"]
MARKET = "^N225"
START = "2013-01-01"
END = "2023-12-31"

INITIAL_CASH = 3000000
STOP_LOSS = -0.07
TRAIL_STOP = -0.12

# 攻めパラメータリスト
RISK_LIST = [0.06, 0.08, 0.10, 0.12, 0.15]
MAX_POS_LIST = [5, 10, 15, 20]

# ===== データ取得 =====
data = yf.download(TICKERS, start=START, end=END)["Close"]
market = yf.download(MARKET, start=START, end=END)["Close"]
if isinstance(market, pd.DataFrame):
    market = market.squeeze()

data = data.reindex(market.index)
ma25_market = market.rolling(25).mean()
ma75_market = market.rolling(75).mean()

# ===== Regime判定 =====
regime = pd.Series(np.where(ma25_market > ma75_market, "BULL", "BEAR"), index=market.index)

# ===== テクニカル =====
ma5 = data.rolling(5).mean()
ma25_data = data.rolling(25).mean()
momentum = data.pct_change(20)
high20 = data.shift(1).rolling(20).max()

# ===== 高速バックテスト関数 =====
def fast_backtest(RISK_PER_TRADE, MAX_POS):
    cash = INITIAL_CASH
    positions = {}
    equity_curve = []

    for date in data.index:
        prices = data.loc[date].dropna()
        if len(prices) == 0:
            equity_curve.append(cash)
            continue

        reg = regime.loc[date]
        max_pos = MAX_POS if reg == "BULL" else 0

        equity = cash + sum([prices[t]*positions[t]["size"] for t in positions if t in prices])
        equity_curve.append(equity)

        # 売却
        remove = []
        for t in positions:
            if t not in prices:
                continue
            entry = positions[t]["entry"]
            peak = positions[t]["peak"]
            price = prices[t]
            ret = price/entry - 1
            if price > peak:
                positions[t]["peak"] = price
                peak = price
            dd = price/peak - 1
            if ret >= 0.5:
                cash += price * positions[t]["size"]/2
                positions[t]["size"]/=2
            if ret <= STOP_LOSS or dd <= TRAIL_STOP:
                cash += price*positions[t]["size"]
                remove.append(t)
        for t in remove:
            positions.pop(t)

        # エントリー
        if len(positions) < max_pos:
            valid = ((ma5.loc[date] > ma25_data.loc[date]) |
                     (momentum.loc[date] > 0.01) |
                     (prices > high20.loc[date]))
            candidates = momentum.loc[date][valid].dropna().sort_values(ascending=False)
            for t in candidates.index:
                if t in positions or t not in prices:
                    continue
                if len(positions) >= max_pos:
                    break
                size = (equity * RISK_PER_TRADE)/prices[t]
                positions[t] = {"entry": prices[t], "size": size, "peak": prices[t]}
                cash -= prices[t]*size

    eq = pd.Series(equity_curve, index=data.index)
    total_return = eq.iloc[-1]/INITIAL_CASH - 1
    years = (eq.index[-1]-eq.index[0]).days / 365
    cagr = (eq.iloc[-1]/INITIAL_CASH)**(1/years)-1
    dd = (eq/eq.cummax()-1).min()
    return eq, total_return, cagr, dd

# ===== 全自動シミュレーション =====
results = []
os.makedirs("simulation_results", exist_ok=True)

for risk in RISK_LIST:
    for max_pos in MAX_POS_LIST:
        eq, total_return, cagr, dd = fast_backtest(RISK_PER_TRADE=risk, MAX_POS=max_pos)
        results.append({
            "RISK": risk,
            "MAX_POS": max_pos,
            "FinalAsset": eq.iloc[-1],
            "TotalReturn": total_return,
            "CAGR": cagr,
            "MaxDD": dd
        })
        # 資産曲線CSV出力
        eq.to_csv(f"simulation_results/eq_r{risk}_pos{max_pos}.csv")

results_df = pd.DataFrame(results)
results_df.to_csv("simulation_results/all_results.csv", index=False)

# ===== 最適パラメータ抽出 =====
best = results_df.loc[results_df["FinalAsset"].idxmax()]
print("\n===== 全自動攻めシミュレーション結果 =====")
print(best)

# グラフ表示
# 修正版
eq_best = pd.read_csv(
    f"simulation_results/eq_r{best.RISK}_pos{int(best.MAX_POS)}.csv", 
    index_col=0, 
    parse_dates=True
).squeeze("columns")
plt.figure(figsize=(12,6))
plt.plot(eq_best, label="資産")
plt.xlabel("日付")
plt.ylabel("資産（円）")
plt.title(f"全自動攻め資産推移 RISK={best.RISK}, MAX_POS={int(best.MAX_POS)}")
plt.ticklabel_format(style='plain', axis='y')
plt.grid(True)
plt.text(eq_best.index[0], eq_best.iloc[0], f"Start: {eq_best.iloc[0]:,.0f}円")
plt.text(eq_best.index[-1], eq_best.iloc[-1], f"End: {eq_best.iloc[-1]:,.0f}円")
plt.legend()
plt.show()
