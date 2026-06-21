    #core/technical/breakout_detector.py

class BreakoutDetector:

    def detect(self, df):

        if len(df) < 60:
            return 0

        high20 = df["High"].rolling(20).max().iloc[-2]
        close = df["Close"].iloc[-1]

        if close > high20:
            return 100

        return 30