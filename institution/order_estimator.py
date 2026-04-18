class OrderEstimator:

    def analyze(self, df):

        score = 0

        close = df["Close"]
        volume = df["Volume"]

        # 上昇日割合
        up = (close.diff() > 0).sum()
        down = (close.diff() < 0).sum()

        if up > down * 1.2:
            score += 40

        # 上昇×出来高
        recent_price = close.pct_change().iloc[-5:]
        recent_vol = volume.iloc[-5:]

        if recent_price.mean() > 0.01 and recent_vol.mean() > volume.mean():
            score += 40

        return score
