import numpy as np


class MarketRegime:

    def detect(self, df):

        try:

            close = df["Close"]

            ma25 = close.rolling(25).mean().iloc[-1]
            ma75 = close.rolling(75).mean().iloc[-1]

            momentum = (
                close.iloc[-1] - close.iloc[-20]
            ) / close.iloc[-20]

            vol = close.pct_change().std()

            # =========================
            # BULL
            # =========================
            if ma25 > ma75 and momentum > 0.05:

                return "BULL"

            # =========================
            # CRASH
            # =========================
            if momentum < -0.12 or vol > 0.05:

                return "CRASH"

            # =========================
            # SIDE
            # =========================
            return "SIDE"

        except:

            return "SIDE"