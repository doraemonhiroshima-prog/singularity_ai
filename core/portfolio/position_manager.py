class PositionManager:

    def style(
        self,
        regime,
        confidence
    ):

        if regime == "BULL":

            if confidence >= 75:
                return "SWING"

            return "DAY"

        if regime == "CRASH":

            return "SHORT"

        return "LONG"