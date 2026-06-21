# core/strategy/adaptive_weights.py

class AdaptiveWeights:

    def get(self, regime):

        # =========================
        # BULL
        # =========================
        if regime == "BULL":

            return {

                "market": 0.10,

                "tech": 0.45,

                "news": 0.10,

                "inst": 0.15,

                "future": 0.20
            }

        # =========================
        # BEAR
        # =========================
        elif regime == "BEAR":

            return {

                "market": 0.30,

                "tech": 0.20,

                "news": 0.10,

                "inst": 0.10,

                "future": 0.30
            }

        # =========================
        # CRASH
        # =========================
        elif regime == "CRASH":

            return {

                "market": 0.45,

                "tech": 0.10,

                "news": 0.05,

                "inst": 0.10,

                "future": 0.30
            }

        # =========================
        # SIDE
        # =========================
        return {

            "market": 0.20,

            "tech": 0.30,

            "news": 0.10,

            "inst": 0.15,

            "future": 0.25
        }