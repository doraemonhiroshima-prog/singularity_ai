import pandas as pd
import glob

print("データ収集開始...")

files = glob.glob("data/*.csv")

all_data = []

for f in files:

    try:
        df = pd.read_csv(f)

        # =========================
        # カラム補正
        # =========================
        if "Close" not in df.columns:
            df.columns = ["Date","Close","High","Low","Open","Volume"]

        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce")

        df = df.dropna()

        if len(df) < 50:
            continue

        # =========================
        # 特徴量作成
        # =========================
        df["Change"] = df["Close"].pct_change()
        df["Future"] = df["Close"].shift(-5)

        df["Label"] = (df["Future"] > df["Close"]).astype(int)

        df["News"] = 0

        df2 = df[["Close","Volume","Change","News","Label"]].dropna()
        df2.columns = ["Price","Volume","Change","News","Label"]

        all_data.append(df2)

    except Exception as e:
        print("ERROR:", f, e)
        continue

# =========================
# 結合
# =========================
final_df = pd.concat(all_data, ignore_index=True)

# =========================
# 保存
# =========================
final_df.to_csv("data/training_data.csv", index=False)

print("学習データ完成:", len(final_df))
