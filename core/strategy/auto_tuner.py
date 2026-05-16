class AutoTuner:

    def __init__(self):

        self.base_threshold = 20

    def threshold(
        self,
        winrate,
        signal_count=10,
        regime="SIDE"
    ):

        try:

            winrate = float(winrate)

            signal_count = int(signal_count)

        except:

            signal_count = 10

            winrate = 0.5

        threshold = self.base_threshold

        # =========================
        # WINRATE
        # =========================
        if winrate > 0.65:

            threshold += 10

        elif winrate < 0.45:

            threshold -= 5

        # =========================
        # SIGNAL COUNT
        # =========================
        if signal_count < 5:

            threshold -= 10

        elif signal_count > 30:

            threshold += 5

        # =========================
        # REGIME
        # =========================
        if regime == "BULL":

            threshold -= 5

        elif regime == "CRASH":

            threshold += 10

        # =========================
        # LIMIT
        # =========================
        threshold = max(
            min(threshold, 80),
            15
        )

        return threshold