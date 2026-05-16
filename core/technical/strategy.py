def sell_signal(df):

    close = df["Close"]

    if close.iloc[-1] < close.iloc[-5]:
        return "SELL"

    return "HOLD"
