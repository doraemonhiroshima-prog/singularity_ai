def sell_signal(df, buy_price, peak_price=None):
    try:
        df = df.copy()

        current_price = float(df["Close"].iloc[-1])

        sma5 = float(df["Close"].rolling(5).mean().iloc[-1])
        sma25 = float(df["Close"].rolling(25).mean().iloc[-1])

        change = (current_price - buy_price) / buy_price

        if change >= 0.2:
            return "TAKE_PROFIT"

        if change <= -0.07:
            return "STOP_LOSS"

        if sma5 < sma25:
            return "TREND_BREAK"

        if peak_price is not None:
            if current_price < peak_price * 0.9:
                return "TRAILING_STOP"

        return "HOLD"

    except Exception as e:
        print(f"SELL ERROR: {e}")
        return "HOLD"
