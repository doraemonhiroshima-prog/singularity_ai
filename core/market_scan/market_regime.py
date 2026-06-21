# core/market_scan/market_regime.py

import numpy as np


class MarketRegime:

    # =====================================================
    # ANALYZE
    # =====================================================
    def analyze(self, df):

        try:

            if len(df) < 80:

                return {

                    "score": 50,

                    "regime": "SIDE"
                }

            close = df["Close"]

            # =============================================
            # MA
            # =============================================
            ma25 = (
                close
                .rolling(25)
                .mean()
                .iloc[-1]
            )

            ma50 = (
                close
                .rolling(50)
                .mean()
                .iloc[-1]
            )

            ma75 = (
                close
                .rolling(75)
                .mean()
                .iloc[-1]
            )

            # =============================================
            # MOMENTUM
            # =============================================
            momentum = (

                close.iloc[-1] -
                close.iloc[-20]

            ) / close.iloc[-20]

            # =============================================
            # VOLATILITY
            # =============================================
            vol = (

                close
                .pct_change()
                .rolling(20)
                .std()
                .iloc[-1]
            )

            # =============================================
            # BULL
            # =============================================
            if (

                ma25 > ma50 and
                ma50 > ma75 and
                momentum > 0.05 and
                vol < 0.04
            ):

                return {

                    "score": 85,

                    "regime": "BULL"
                }

            # =============================================
            # CRASH
            # =============================================
            if (

                momentum < -0.12 or
                vol > 0.05
            ):

                return {

                    "score": 15,

                    "regime": "CRASH"
                }

            # =============================================
            # BEAR
            # =============================================
            if ma25 < ma75:

                return {

                    "score": 30,

                    "regime": "BEAR"
                }

            # =============================================
            # SIDE
            # =============================================
            return {

                "score": 50,

                "regime": "SIDE"
            }

        except Exception as e:

            print(
                "REGIME ERROR:",
                e
            )

            return {

                "score": 50,

                "regime": "SIDE"
            }