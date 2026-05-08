class PredictAI:

    def predict(self, df):

        try:

            if len(df) < 25:
                return 50

            ma5 = df["Close"].rolling(5).mean().iloc[-1]
            ma25 = df["Close"].rolling(25).mean().iloc[-1]

            if ma25 == 0:
                return 50

            diff = (ma5 - ma25) / ma25

            score = 50 + diff * 500

            score = max(0, min(100, score))

            return score

        except:

            return 50