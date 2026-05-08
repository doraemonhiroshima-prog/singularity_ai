class InstitutionAI:

    def run(self, df):

        try:

            vol = df["Volume"]

            recent = vol.iloc[-5:].mean()

            old = vol.iloc[-30:-5].mean()

            if old == 0:
                return 50

            ratio = recent / old

            score = ratio * 50

            return max(
                min(score, 100),
                0
            )

        except:

            return 50