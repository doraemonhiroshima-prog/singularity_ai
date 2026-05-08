class AutoTuner:

    def threshold(self, winrate):

        # =========================
        # GOOD
        # =========================
        if winrate > 0.65:
            return 55

        # =========================
        # NORMAL
        # =========================
        if winrate > 0.50:
            return 45

        # =========================
        # BAD
        # =========================
        return 35