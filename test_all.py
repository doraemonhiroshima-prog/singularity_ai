from ai.market_scan.market_scan_ai import MarketScanAI
from ai.technical.technical_runner import TechnicalAI
from ai.Future_prediction.predict_ai import PredictAI
import pandas as pd

print("=== 全銘柄スキャン ===")

# 銘柄リスト
df_list = pd.read_csv("data/stock_list.csv")

market = MarketScanAI()
tech = TechnicalAI()
future_ai = PredictAI()

results = []

for _, row in df_list.iterrows():

    code = row["code"]
    name = row.get("name", "")

    try:
        data = market.fetch_one({"code": code, "name": name})

        if not data or "df" not in data:
            continue

        df = data["df"]

        close = df["Close"]
        volume = df["Volume"]

        price = float(close.iloc[-1])
        vol = float(volume.iloc[-1])
        change = float(close.pct_change().iloc[-1])

        prob = future_ai.predict(price, vol, change, 0)

        results.append({
            "code": code,
            "prob": prob
        })

    except:
        continue

# =========================
# ランキング
# =========================
results = sorted(results, key=lambda x: x["prob"], reverse=True)

print("\n=== TOP10 ===")

for r in results[:10]:
    print(r)
