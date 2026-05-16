import numpy as np


class Scorer:

    def __init__(self):

        self.score_history = []

    # =========================
    # SAFE
    # =========================
    def safe(self, value):

        try:

            value = float(value)

            return max(
                min(value, 100),
                0
            )

        except:

            return 50

    # =========================
    # REGIME WEIGHTS
    # =========================
    def regime_weights(
        self,
        regime
    ):

        if regime == "BULL":

            return {
                "technical": 0.35,
                "institution": 0.20,
                "news": 0.15,
                "future": 0.20,
                "market": 0.10
            }

        if regime == "CRASH":

            return {
                "technical": 0.10,
                "institution": 0.45,
                "news": 0.15,
                "future": 0.20,
                "market": 0.10
            }

        return {
            "technical": 0.25,
            "institution": 0.25,
            "news": 0.15,
            "future": 0.25,
            "market": 0.10
        }

    # =========================
    # SCORE
    # =========================
    def calculate(
        self,
        data,
        regime="SIDE"
    ):

        w = self.regime_weights(
            regime
        )

        technical = self.safe(
            data.get("technical", 50)
        )

        institution = self.safe(
            data.get("institution", 50)
        )

        news = self.safe(
            data.get("news", 50)
        )

        future = self.safe(
            data.get("future", 50)
        )

        market = self.safe(
            data.get("market", 50)
        )

        score = (
            technical * w["technical"] +
            institution * w["institution"] +
            news * w["news"] +
            future * w["future"] +
            market * w["market"]
        )

        # =========================
        # SMART BOOST
        # =========================
        if (
            technical >= 70 and
            institution >= 70
        ):
            score += 5

        if (
            news >= 70 and
            future >= 70
        ):
            score += 5

        # =========================
        # OVERHEAT
        # =========================
        if technical > 90:
            score -= 5

        score = round(
            max(min(score, 100), 0),
            2
        )

        self.score_history.append(score)

        self.score_history = (
            self.score_history[-1000:]
        )

        return score

    # =========================
    # DISTRIBUTION
    # =========================
    def distribution(self):

        if len(self.score_history) < 20:

            return {
                "mean": 50,
                "std": 10
            }

        return {
            "mean": round(
                np.mean(self.score_history),
                2
            ),
            "std": round(
                np.std(self.score_history),
                2
            )
        }