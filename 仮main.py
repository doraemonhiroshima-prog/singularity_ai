from technical import TechnicalAI
from market_scan.data_fetcher import fetch_data
import pandas as pd

ai = TechnicalAI()

df_codes = pd.read_csv("stock_list.csv")
codes = df_codes["Code"].astype(str) + ".T"

data = fetch_data(codes)

results = []

for code, df in data.items():
    result = ai.process(df)
    results.append((code, result["score"], result["signal"]))

results.sort(key=lambda x: x[1], reverse=True)

print("=== RANKING ===")
for r in results[:10]:
    print(r)
