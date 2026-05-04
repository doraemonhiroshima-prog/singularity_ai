class PressureAnalyzer:

    def analyze(self, df):

        score = 0

        c = df["Close"].iloc[-1]
        o = df["Open"].iloc[-1]
        h = df["High"].iloc[-1]
        l = df["Low"].iloc[-1]

        body = abs(c - o)
        rng = h - l

        if rng > 0:

            power = body / rng

            if c > o and power > 0.7:
                score += 40

            elif c < o and power > 0.7:
                score -= 40

        return score
