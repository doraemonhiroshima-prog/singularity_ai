class InstitutionCore:

    def analyze(self, df):

        try:
            vol = df["Volume"].iloc[-1]
            avg = df["Volume"].rolling(20).mean().iloc[-1]

            if avg == 0:
                return 50

            ratio = vol / avg

            return min(100, ratio * 50)

        except:
            return 50