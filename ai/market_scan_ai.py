from core.market_scan.market_regime import MarketRegime


class MarketScanAI:

    def __init__(self):
        self.regime = MarketRegime()

    def run(self, df):

        try:

            regime = self.regime.analyze(df)

            close = df["Close"]

            ma25 = close.rolling(25).mean().iloc[-1]

            current = close.iloc[-1]

            score = 50

            if regime["regime"] == "bull":
                score += 25

            elif regime["regime"] == "bear":
                score -= 25

            if current > ma25:
                score += 15
            else:
                score -= 15

            return max(min(score, 100), 0)

        except:
            return 50