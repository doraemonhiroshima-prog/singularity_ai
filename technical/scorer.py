def analyze_stock(df, news_score=0):
    try:
        if df is None or len(df) < 30:
            return 0

        df = df.copy()
        latest = df.iloc[-1]

        # 安全に値取得
        close = float(latest["Close"])
        sma5 = float(latest["SMA5"])
        sma25 = float(latest["SMA25"])
        rsi = float(latest["RSI"])

        score = 0

        # =========================
        # TREND
        # =========================
        if sma5 > sma25:
            score += 30
        elif sma5 > sma25 * 0.98:
            score += 15

        # =========================
        # PRICE POSITION
        # =========================
        if close > sma5:
            score += 20
        elif close > sma5 * 0.98:
            score += 10

        # =========================
        # MOMENTUM
        # =========================
        if df["Close"].iloc[-1] > df["Close"].iloc[-2]:
            score += 10

        if df["Close"].iloc[-1] > df["Close"].iloc[-5]:
            score += 15

        # =========================
        # VOLUME
        # =========================
        if "Volume" in df.columns:
            vol = float(latest["Volume"])
            vol_avg = float(df["Volume"].rolling(5).mean().iloc[-1])

            if vol > vol_avg * 1.5:
                score += 25
            elif vol > vol_avg * 1.2:
                score += 10

        # =========================
        # RSI
        # =========================
        if 40 < rsi < 65:
            score += 15
        elif 35 < rsi < 70:
            score += 5

        if rsi > 75:
            score -= 15

        # =========================
        # NEWS
        # =========================
        if news_score > 0.2:
            score += 20
        elif news_score < -0.2:
            score -= 20

        return int(score)

    except Exception as e:
        print(f"SCAN ERROR: {e}")
        return 0
