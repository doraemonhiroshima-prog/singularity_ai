class CapitalManager:

    def cash_ratio(
        self,
        regime
    ):

        if regime == "BULL":
            return 0.10

        if regime == "CRASH":
            return 0.70

        return 0.30

    def max_positions(
        self,
        regime
    ):

        if regime == "BULL":
            return 15

        if regime == "CRASH":
            return 5

        return 10