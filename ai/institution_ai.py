# ai/institution_ai.py

class InstitutionAI:

    def run(self, df):

        try:

            # =========================
            # VOLUME CHECK
            # =========================
            if "Volume" not in df.columns:
                return {
                    "score": 50
                }

            if len(df) < 20:
                return {
                    "score": 50
                }

            # =========================
            # CURRENT VOLUME
            # =========================
            vol_now = float(
                df["Volume"].iloc[-1]
            )

            # =========================
            # AVG VOLUME
            # =========================
            vol_avg = float(
                df["Volume"]
                .rolling(20)
                .mean()
                .iloc[-1]
            )

            if vol_avg <= 0:

                return {
                    "score": 50
                }

            # =========================
            # RATIO
            # =========================
            ratio = vol_now / vol_avg

            score = 50

            # =========================
            # BIG MONEY DETECT
            # =========================
            if ratio > 3.0:

                score += 50

            elif ratio > 2.0:

                score += 40

            elif ratio > 1.5:

                score += 25

            elif ratio > 1.2:

                score += 10

            # =========================
            # PRICE + VOLUME
            # =========================
            close = df["Close"]

            momentum = (
                close.iloc[-1] -
                close.iloc[-5]
            ) / close.iloc[-5]

            if momentum > 0.10 and ratio > 1.5:

                score += 20

            elif momentum > 0.05 and ratio > 1.2:

                score += 10

            # =========================
            # LIMIT
            # =========================
            score = max(
                min(score, 100),
                0
            )

            return {

                "score": score,

                "volume_ratio": ratio,

                "momentum": momentum
            }

        except Exception as e:

            print(
                "INSTITUTION AI ERROR:",
                e
            )

            return {
                "score": 50
            }