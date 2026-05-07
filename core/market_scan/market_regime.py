class MarketRegime:

    def analyze(self, nikkei_df):

        if len(nikkei_df) < 50:
            return {
                "score": 50,
                "regime": "neutral"
            }

        ma25 = nikkei_df["Close"].rolling(25).mean().iloc[-1]
        ma50 = nikkei_df["Close"].rolling(50).mean().iloc[-1]

        if ma50 == 0:
            return {
                "score": 50,
                "regime": "neutral"
            }

        if ma25 > ma50:

            return {
                "score": 80,
                "regime": "bull"
            }

        return {
            "score": 30,
            "regime": "bear"
        }