class CrashDetector:

    def detect(self, df):

        if len(df) < 25:
            return 0

        ma5 = df["Close"].rolling(5).mean().iloc[-1]
        ma25 = df["Close"].rolling(25).mean().iloc[-1]

        if ma25 == 0:
            return 0

        diff = (ma5 - ma25) / ma25

        if diff < -0.08:
            return 100

        return 0