def add_indicators(df):
    df = df.copy()

    df["SMA5"] = df["Close"].rolling(5).mean()
    df["SMA25"] = df["Close"].rolling(25).mean()

    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))


    return df
