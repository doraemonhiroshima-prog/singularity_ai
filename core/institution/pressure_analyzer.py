# core/institution/pressure_analyzer.py

class PressureAnalyzer:

    # =====================================================
    # ANALYZE
    # =====================================================
    def analyze(self, df):

        try:

            if len(df) < 30:

                return {
                    "score": 50
                }

            close = df["Close"]

            volume = df["Volume"]

            current = float(
                close.iloc[-1]
            )

            low10 = float(
                close.iloc[-10:].min()
            )

            drop = (
                current - low10
            ) / low10

            vol_now = float(
                volume.iloc[-1]
            )

            vol20 = float(
                volume
                .rolling(20)
                .mean()
                .iloc[-1]
            )

            score = 50

            # =================================================
            # ABSORPTION
            # =================================================
            if (
                vol_now > vol20 * 1.5 and
                drop > -0.03
            ):

                score += 30

            # =================================================
            # PRICE HOLD
            # =================================================
            if current >= close.iloc[-5]:

                score += 10

            # =================================================
            # DRY UP
            # =================================================
            dry = 0

            for i in range(1, 6):

                if close.iloc[-i] < close.iloc[-i - 1]:

                    current_vol = float(
                        volume.iloc[-i]
                    )

                    avg_vol = float(
                        volume
                        .rolling(20)
                        .mean()
                        .iloc[-i]
                    )

                    if current_vol < avg_vol:

                        dry += 1

            score += dry * 5

            score = max(
                min(score, 100),
                0
            )

            return {

                "score": score,

                "drop": drop,

                "dry": dry
            }

        except Exception as e:

            print(
                "PRESSURE ERROR:",
                e
            )

            return {
                "score": 50
            }