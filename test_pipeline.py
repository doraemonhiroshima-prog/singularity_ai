import pandas as pd

from ai.technical.technical_runner import TechnicalAI
from news.news_ai import NewsAI
from ai.institution.institution_ai import InstitutionAI
from ai.Future_prediction.predict_ai import PredictAI


# =========================
# データ読み込み
# =========================
df = pd.read_csv("data/7203.T.csv")

# =========================
# 列ズレ応急処置
# =========================
if "Close" not in df.columns:
    df.columns = ["Date","Close","High","Low","Open","Volume"]

# =========================
# ★ 数値変換（超重要）
# =========================
for col in ["Open", "High", "Low", "Close", "Volume"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# 欠損削除
df = df.dropna()

# =========================
# AI初期化
# =========================
tech = TechnicalAI()
news = NewsAI()
inst = InstitutionAI()
future = PredictAI()

# =========================
# 実行
# =========================
print("\n=== TECHNICAL ===")
t = tech.process(df)
print(t)

print("\n=== NEWS ===")
n = news.analyze("7203.T", "トヨタ")
print(n)

print("\n=== INSTITUTION ===")
i = inst.analyze(df)
print(i)

print("\n=== FUTURE ===")
f = future.process(df)
print(f)

print("\n=== 完了 ===")
