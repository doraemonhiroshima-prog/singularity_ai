class FlowDetector:

    def analyze(self, df):

        score = 0

        v_now = df["Volume"].iloc[-1]
        v_avg20 = df["Volume"].rolling(20).mean().iloc[-1]

        if v_avg20 > 0:
            ratio = v_now / v_avg20

            if ratio > 2.5:
                score += 60
            elif ratio > 2:
                score += 40
            elif ratio > 1.5:
                score += 20

        # 継続流入（重要）
        vol_trend = df["Volume"].rolling(5).mean().iloc[-5:]

        if vol_trend.is_monotonic_increasing:
            score += 30

        return score
