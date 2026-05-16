import numpy as np


class MarketRegime:

    def detect(self, df):

        try:

            if len(df) < 80:
                return "SIDE"

            close = df["Close"]

            ma25 = (
                close
                .rolling(25)
                .mean()
                .iloc[-1]
            )

            ma75 = (
                close
                .rolling(75)
                .mean()
                .iloc[-1]
            )

            momentum = (
                close.iloc[-1] -
                close.iloc[-20]
            ) / close.iloc[-20]

            # =========================
            # 直近ボラ
            # =========================
            vol = (
                close
                .pct_change()
                .rolling(20)
                .std()
                .iloc[-1]
            )

            # =========================
            # BULL
            # =========================
            if (
                ma25 > ma75 and
                momentum > 0.05 and
                vol < 0.04
            ):

                return "BULL"

            # =========================
            # CRASH
            # =========================
            if (
                momentum < -0.12 or
                vol > 0.05
            ):

                return "CRASH"

            # =========================
            # SIDE
            # =========================
            return "SIDE"

        except Exception as e:

            print("REGIME ERROR:", e)

            return "SIDE"