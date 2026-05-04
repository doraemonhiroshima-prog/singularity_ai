import pandas as pd

def clean_df(df):

    # =========================
    # 列名小文字化
    # =========================
    df.columns = [c.lower() for c in df.columns]

    # =========================
    # 列名マッピング
    # =========================
    col_map = {
        "date": "Date",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume"
    }

    df = df.rename(columns=col_map)

    # =========================
    # 必須列チェック
    # =========================
    required = ["Open", "High", "Low", "Close"]

    for r in required:
        if r not in df.columns:
            print("❌ 欠損列:", r)
            return pd.DataFrame()

    # =========================
    # 数値変換
    # =========================
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # =========================
    # 日付処理
    # =========================
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        df = df.sort_values("Date")

    # =========================
    # NaN削除
    # =========================
    df = df.dropna()

    return df
