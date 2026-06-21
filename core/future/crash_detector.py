# core/future/crash_detector.py

class CrashDetector:

    # =====================================================
    # DETECT
    # =====================================================
    def detect(
        self,
        df
    ):

        try:

            if len(df) < 50:

                return {
                    "risk": 0,
                    "crash": False
                }

            close = df["Close"]

            ma5 = (
                close
                .rolling(5)
                .mean()
                .iloc[-1]
            )

            ma25 = (
                close
                .rolling(25)
                .mean()
                .iloc[-1]
            )

            momentum = (

                close.iloc[-1] -
                close.iloc[-20]

            ) / close.iloc[-20]

            volatility = (

                close
                .pct_change()
                .rolling(20)
                .std()
                .iloc[-1]
            )

            if ma25 == 0:

                return {
                    "risk": 0,
                    "crash": False
                }

            diff = (
                ma5 - ma25
            ) / ma25

            risk = 0

            # =============================================
            # TREND BREAK
            # =============================================
            if diff < -0.03:

                risk += 25

            if diff < -0.08:

                risk += 40

            # =============================================
            # MOMENTUM
            # =============================================
            if momentum < -0.10:

                risk += 25

            # =============================================
            # VOLATILITY
            # =============================================
            if volatility > 0.05:

                risk += 20

            risk = max(
                min(risk, 100),
                0
            )

            return {

                "risk": float(risk),

                "crash": risk >= 60
            }

        except Exception as e:

            print(
                "CRASH DETECTOR ERROR:",
                e
            )

            return {

                "risk": 0,

                "crash": False
            }