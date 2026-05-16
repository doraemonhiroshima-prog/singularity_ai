class StrategyCore:

    def build(
        self,
        regime,
        weights,
        threshold
    ):

        return {
            "regime": regime,
            "weights": weights,
            "threshold": threshold
        }