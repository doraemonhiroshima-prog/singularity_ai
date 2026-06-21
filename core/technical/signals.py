     #core/technical/signals.py

def volume_score(df):
    latest = df.iloc[-1]

    vol = latest["Volume"]
    vol_avg = df["Volume"].rolling(5).mean().iloc[-1]

    if vol > vol_avg * 1.5:
        return 40
    elif vol > vol_avg * 1.2:
        return 20
    return 0


def breakout_score(df):
    latest = df.iloc[-1]

    high_20 = df["High"].rolling(20).max().iloc[-1]
    high_10 = df["High"].rolling(10).max().iloc[-1]

    if latest["Close"] > high_20:
        return 50
    elif latest["Close"] > high_10:
        return 25
    return 0