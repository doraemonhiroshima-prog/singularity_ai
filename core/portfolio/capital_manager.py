class CapitalManager:

    def __init__(self):

        # =========================
        # LEARNING MEMORY
        # =========================
        self.regime_memory = {

            "BULL": 1.0,
            "RANGE": 1.0,
            "CRASH": 1.0
        }

    # =========================
    # CASH RATIO
    # =========================
    def cash_ratio(
        self,
        regime,
        volatility=0,
        drawdown=0
    ):

        # =========================
        # BASE
        # =========================
        if regime == "BULL":

            cash = 0.05

        elif regime == "CRASH":

            cash = 0.50

        else:

            cash = 0.20

        # =========================
        # VOLATILITY CONTROL
        # =========================
        if volatility > 0.05:

            cash += 0.10

        elif volatility > 0.03:

            cash += 0.05

        # =========================
        # DRAWDOWN CONTROL
        # =========================
        if drawdown > 0.20:

            cash += 0.15

        elif drawdown > 0.10:

            cash += 0.08

        # =========================
        # REGIME LEARNING
        # =========================
        memory = self.regime_memory.get(
            regime,
            1.0
        )

        cash *= (2 - memory)

        # =========================
        # LIMIT
        # =========================
        cash = max(
            min(cash, 0.80),
            0.02
        )

        return cash

    # =========================
    # MAX POSITIONS
    # =========================
    def max_positions(
        self,
        regime,
        confidence=0
    ):

        # =========================
        # BASE
        # =========================
        if regime == "BULL":

            positions =24

        elif regime == "CRASH":

            positions = 6

        else:

            positions =18

        # =========================
        # CONFIDENCE EXPANSION
        # =========================
        if confidence >= 85:

            positions += 2

        elif confidence >= 75:

            positions += 1

        return positions

    # =========================
    # REGIME LEARNING UPDATE
    # =========================
    def update_learning(
        self,
        regime,
        pnl
    ):

        old = self.regime_memory.get(
            regime,
            1.0
        )

        score = 1 + pnl

        new = (
            old * 0.9 +
            score * 0.1
        )

        new = max(
            min(new, 1.5),
            0.5
        )

        self.regime_memory[regime] = new