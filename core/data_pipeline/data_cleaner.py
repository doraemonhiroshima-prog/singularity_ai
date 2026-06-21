   #core/data_pipeline/data_cleaner.py

import pandas as pd


def clean_df(df):

    # =========================
    # 列名統一
    # =========================
    df.columns = [str(c).strip().lower() for c in df.columns]

    # =========================
    # カラム変換
    # =========================
    rename_map = {
        "date": "Date",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    }

    df = df.rename(columns=rename_map)

    # =========================
    # 必須列
    # =========================
    required = ["Date", "Open", "High", "Low", "Close"]

    missing = [c for c in required if c not in df.columns]

    if missing:
        print("❌ 欠損:", missing)
        return pd.DataFrame()

    # =========================
    # 数値変換
    # =========================
    numeric_cols = ["Open", "High", "Low", "Close"]

    if "Volume" in df.columns:
        numeric_cols.append("Volume")

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # =========================
    # 日付
    # =========================
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # =========================
    # NaN削除
    # =========================
    df = df.dropna()

    # =========================
    # 日付順
    # =========================
    df = df.sort_values("Date").reset_index(drop=True)

    return df