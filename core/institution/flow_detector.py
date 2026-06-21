# core/institution/flow_detector.py

class FlowDetector:

    # =====================================================
    # DETECT
    # =====================================================
    def detect(self, df):

        try:

            if len(df) < 60:

                return {
                    "score": 50
                }

            close = df["Close"]

            volume = df["Volume"]

            current = float(
                close.iloc[-1]
            )

            # =================================================
            # VOLUME
            # =================================================
            vol5 = float(
                volume
                .rolling(5)
                .mean()
                .iloc[-1]
            )

            vol20 = float(
                volume
                .rolling(20)
                .mean()
                .iloc[-1]
            )

            vol60 = float(
                volume
                .rolling(60)
                .mean()
                .iloc[-1]
            )

            score = 50

            # =================================================
            # FLOW EXPANSION
            # =================================================
            if (
                vol5 > vol20 and
                vol20 > vol60
            ):

                score += 20

            # =================================================
            # FLOW ACCELERATION
            # =================================================
            if vol20 > 0:

                ratio = vol5 / vol20

                if ratio > 3.0:

                    score += 30

                elif ratio > 2.0:

                    score += 20

                elif ratio > 1.5:

                    score += 10

            # =================================================
            # STEALTH ACCUMULATION
            # =================================================
            high20 = float(
                close.iloc[-20:].max()
            )

            low20 = float(
                close.iloc[-20:].min()
            )

            range_ratio = (
                high20 - low20
            ) / low20

            if (
                range_ratio < 0.08 and
                vol5 > vol20 * 1.5
            ):

                score += 20

            # =================================================
            # BREAKOUT VOLUME
            # =================================================
            high50 = float(
                close.iloc[-50:-1].max()
            )

            vol_now = float(
                volume.iloc[-1]
            )

            if (
                current > high50 and
                vol_now > vol20 * 1.5
            ):

                score += 20

            score = max(
                min(score, 100),
                0
            )

            return {

                "score": score,

                "vol5": vol5,

                "vol20": vol20,

                "vol60": vol60,

                "range_ratio": range_ratio
            }

        except Exception as e:

            print(
                "FLOW DETECTOR ERROR:",
                e
            )

            return {
                "score": 50
            }