# core/institution/order_estimator.py

class OrderEstimator:

    # =====================================================
    # ESTIMATE
    # =====================================================
    def estimate(self, df):

        try:

            if len(df) < 20:

                return {
                    "score": 50
                }

            close = df["Close"]

            volume = df["Volume"]

            score = 50

            # =================================================
            # VWAP
            # =================================================
            value = (
                close * volume
            ).rolling(20).sum()

            vol = (
                volume
            ).rolling(20).sum()

            vwap = (
                value.iloc[-1] /
                (vol.iloc[-1] + 1e-9)
            )

            current = float(
                close.iloc[-1]
            )

            if current > vwap:

                score += 20

            diff = (
                current - vwap
            ) / vwap

            if diff > 0.05:

                score += 10

            # =================================================
            # BUY PRESSURE
            # =================================================
            pressure = 0

            for i in range(1, 11):

                if (
                    close.iloc[-i] >=
                    close.iloc[-i - 1]
                ):

                    pressure += 1

            score += pressure * 2

            # =================================================
            # VOLUME SUPPORT
            # =================================================
            vol_now = float(
                volume.iloc[-1]
            )

            vol20 = float(
                volume
                .rolling(20)
                .mean()
                .iloc[-1]
            )

            if vol20 > 0:

                ratio = (
                    vol_now / vol20
                )

                if ratio > 2:

                    score += 15

                elif ratio > 1.5:

                    score += 10

            score = max(
                min(score, 100),
                0
            )

            return {

                "score": score,

                "vwap": vwap,

                "pressure": pressure
            }

        except Exception as e:

            print(
                "ORDER ESTIMATOR ERROR:",
                e
            )

            return {
                "score": 50
            }