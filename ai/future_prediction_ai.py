class FuturePredictionAI:

    def run(self, df):

        try:

            close = df["Close"]

            now = close.iloc[-1]

            ma5 = close.rolling(5).mean().iloc[-1]

            ma20 = close.rolling(20).mean().iloc[-1]

            momentum = (
                close.iloc[-1] -
                close.iloc[-10]
            ) / close.iloc[-10]

            score = 50

            if ma5 > ma20:
                score += 20

            if momentum > 0.05:
                score += 20

            elif momentum < -0.05:
                score -= 20

            if now > ma5:
                score += 10

            return max(
                min(score, 100),
                0
            )

        except:

            return 50