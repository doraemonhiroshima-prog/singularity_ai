class InstitutionAI:

    def run(self, df):

        try:

            if "Volume" not in df.columns:
                return 50

            vol_now = df["Volume"].iloc[-1]

            vol_avg = (
                df["Volume"]
                .rolling(20)
                .mean()
                .iloc[-1]
            )

            if vol_avg <= 0:
                return 50

            ratio = vol_now / vol_avg

            score = 50

            if ratio > 2.0:
                score += 40

            elif ratio > 1.5:
                score += 25

            elif ratio > 1.2:
                score += 10

            return max(
                min(score, 100),
                0
            )

        except:

            return 50