import glob
import pandas as pd
import os


SAVE_PATH = "data/training_data.csv"


def build_training_data():

    print("読み込み中...")

    files = glob.glob("data/*.csv")

    data = []

    for f in files:

        if "training_data" in f or "stock_list" in f:
            continue

        try:
            df = pd.read_csv(f)

            # 必須列チェック
            if not {"Close", "Volume"}.issubset(df.columns):
                continue

            # 特徴量生成
            df["return"] = df["Close"].pct_change()
            df["vol_change"] = df["Volume"].pct_change()

            df["ma5"] = df["Close"].rolling(5).mean()
            df["ma25"] = df["Close"].rolling(25).mean()

            df["target"] = df["Close"].shift(-1) > df["Close"]
            df = df.replace([float("inf"), float("-inf")], None)
            df = df.dropna()

            if len(df) == 0:
                continue

            data.append(df)

        except Exception as e:
            print("SKIP:", f, e)

    if len(data) == 0:
        print("データなし")
        return

    full = pd.concat(data)

    print("データ数:", len(full))

    # サイズ制限（重すぎ防止）
    if len(full) > 50000:
        full = full.sample(50000)

    print("学習データ:", len(full))

    full.to_csv(SAVE_PATH, index=False)

    print("保存完了")
