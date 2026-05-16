class AdaptiveWeights:

    def get(self, regime):

        # =========================
        # BULL
        # =========================
        if regime == "BULL":

            return {
                "market": 0.05,
                "tech": 0.80,
                "news": 0.05,
                "inst": 0.05,
                "future": 0.05
            }

        # =========================
        # CRASH
        # =========================
        if regime == "CRASH":

            return {
                "market": 0.10,
                "tech": 0.70,
                "news": 0.05,
                "inst": 0.10,
                "future": 0.05
            }

        # =========================
        # SIDE
        # =========================
        return {
            "market": 0.05,
            "tech": 0.80,
            "news": 0.05,
            "inst": 0.05,
            "future": 0.05
        }