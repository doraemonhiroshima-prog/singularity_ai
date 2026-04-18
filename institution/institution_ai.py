class InstitutionAI:

    def analyze(self, df):

        try:
            volume = df["Volume"]

            vol_now = float(volume.iloc[-1].item())
            vol_avg = float(volume.rolling(10).mean().iloc[-1].item())


            score = 0

            if vol_now > vol_avg * 1.5:
                score += 20

            if vol_now > vol_avg * 2:
                score += 50

            if vol_now > vol_avg * 3:
                score += 80

            return score

        except:
            return 0
