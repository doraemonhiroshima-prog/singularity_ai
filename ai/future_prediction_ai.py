class FuturePredictionAI:

    def run(self, df):

        try:

            close = df["Close"]

            future = (
                close.iloc[-1] -
                close.iloc[-20]
            ) / close.iloc[-20]

            score = 50 + future * 300

            return max(
                min(score, 100),
                0
            )

        except:

            return 50