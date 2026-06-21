     #fix_data.py
     

import pandas as pd
import glob
import os

files = glob.glob("data/*.csv")

for f in files:

    if "training_data" in f or "stock_list" in f or "learning" in f:
        continue

    try:
        df = pd.read_csv(f)

        # MultiIndex解除
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # 不要列削除（Tickerなど）
        df = df.loc[:, ~df.columns.duplicated()]

        # 必須列だけ残す
        keep = []

        for col in df.columns:
            if col in ["Date","Close","High","Low","Open","Volume"]:
                keep.append(col)

        df = df[keep]

        # 数値変換
        for col in ["Close","High","Low","Open","Volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        df = df.dropna()

        # 上書き保存
        df.to_csv(f, index=False)

        print("FIXED:", f)

    except Exception as e:
        print("ERROR:", f, e)
