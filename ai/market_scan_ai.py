class MarketScanAI:

    def run(self, df):

        try:

            close = df["Close"]

            ma25 = close.rolling(25).mean().iloc[-1]

            current = close.iloc[-1]

            diff = (
                (current - ma25) / ma25
            ) * 100

            score = 50 + diff * 5

            return max(
                min(score, 100),
                0
            )

        except:

            return 50