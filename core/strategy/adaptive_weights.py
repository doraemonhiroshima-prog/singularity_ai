class AdaptiveWeights:

    def get(self, regime):

        # =========================
        # BULL
        # =========================
        if regime == "BULL":

            return {
                "market": 0.15,
                "tech": 0.40,
                "news": 0.15,
                "inst": 0.10,
                "future": 0.20
            }

        # =========================
        # CRASH
        # =========================
        if regime == "CRASH":

            return {
                "market": 0.10,
                "tech": 0.10,
                "news": 0.10,
                "inst": 0.45,
                "future": 0.25
            }

        # =========================
        # SIDE
        # =========================
        return {
            "market": 0.15,
            "tech": 0.25,
            "news": 0.20,
            "inst": 0.20,
            "future": 0.20
        }