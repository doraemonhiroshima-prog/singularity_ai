import yfinance as yf
import pandas as pd
import os
import time

# =========================
# 設定
# =========================
CSV_PATH = "data/stock_list.csv"
SAVE_DIR = "data"

START = "2005-01-01"   # 20年
SLEEP = 2              # 通常待機
ERROR_SLEEP = 8        # エラー時
BATCH_SIZE = 20        # バッチ単位
BATCH_SLEEP = 30       # 休憩

os.makedirs(SAVE_DIR, exist_ok=True)

# =========================
# 銘柄読み込み
# =========================
df_list = pd.read_csv(CSV_PATH)
codes = df_list["code"].tolist()

print(f"総銘柄数: {len(codes)}")

# =========================
# 取得処理
# =========================
for i, code in enumerate(codes):

    path = os.path.join(SAVE_DIR, f"{code}.csv")

    try:
        print(f"DL: {code} ({i+1}/{len(codes)})")

        df = yf.download(
            code,
            start=START,
            interval="1d",
            progress=False,
            auto_adjust=True
        )

        # =========================
        # データチェック
        # =========================
        if df is None or df.empty:
            print(f"NG: {code}")
            continue

        # =========================
        # ★ 重要修正
        # =========================
        df = df[["Open", "High", "Low", "Close", "Volume"]]
        df.reset_index(inplace=True)

        # =========================
        # 保存
        # =========================
        df.to_csv(path, index=False)

        time.sleep(SLEEP)

    except Exception as e:
        print(f"ERROR: {code} {e}")
        time.sleep(ERROR_SLEEP)

    # =========================
    # バッチ休憩
    # =========================
    if (i + 1) % BATCH_SIZE == 0:
        print("=== 休憩 ===")
        time.sleep(BATCH_SLEEP)

print("=== 20年データ取得完了（修正版） ===")
