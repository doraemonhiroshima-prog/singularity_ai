from core.strategy.market_regime import MarketRegime


class MarketScanAI:

    def __init__(self):

        self.regime = MarketRegime()

    def run(self, df):

        try:

            regime = self.regime.detect(df)

            close = df["Close"]

            ma25 = close.rolling(25).mean().iloc[-1]

            current = close.iloc[-1]

            score = 50

            # 上昇相場
            if regime == "BULL":
                score += 25

            # 暴落
            elif regime == "CRASH":
                score -= 25

            # MA上
            if current > ma25:
                score += 15

            else:
                score -= 15

            return max(
                min(score, 100),
                0
            )

        except:

            return 50