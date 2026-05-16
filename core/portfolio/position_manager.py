class PositionManager:

    def __init__(self):

        # =========================
        # POSITION MEMORY
        # =========================
        self.position_memory = {}

    # =========================
    # POSITION STYLE
    # =========================
    def style(
        self,
        regime,
        confidence,
        volatility=0,
        momentum=0
    ):

        # =========================
        # BULL
        # =========================
        if regime == "BULL":

            if confidence >= 85:

                return "TREND"

            elif confidence >= 70:

                return "SWING"

            return "DAY"

        # =========================
        # CRASH
        # =========================
        if regime == "CRASH":

            if volatility > 0.05:

                return "SCALP"

            return "SHORT"

        # =========================
        # RANGE
        # =========================
        if momentum > 0:

            return "LONG"

        return "MEAN_REVERT"

    # =========================
    # POSITION WEIGHT
    # =========================
    def weight(
        self,
        confidence,
        memory_score=0,
        pnl=0
    ):

        weight = 1.0

        # =========================
        # CONFIDENCE
        # =========================
        if confidence >= 90:

            weight += 0.50

        elif confidence >= 80:

            weight += 0.30

        elif confidence >= 70:

            weight += 0.15

        # =========================
        # MEMORY BOOST
        # =========================
        if memory_score > 0:

            weight += min(
                memory_score,
                0.30
            )

        # =========================
        # WINNER PYRAMID
        # =========================
        if pnl > 0.10:

            weight += 0.20

        elif pnl > 0.20:

            weight += 0.40

        return weight

    # =========================
    # UPDATE LEARNING
    # =========================
    def update_learning(
        self,
        code,
        pnl
    ):

        old = self.position_memory.get(
            code,
            0
        )

        new = (
            old * 0.9 +
            pnl * 0.1
        )

        self.position_memory[code] = new