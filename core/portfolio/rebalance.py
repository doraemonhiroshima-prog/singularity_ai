class RebalanceManager:

    def __init__(self):

        # =========================
        # REBALANCE MEMORY
        # =========================
        self.rebalance_memory = {}

    # =========================
    # REBALANCE
    # =========================
    def rebalance(
        self,
        holdings,
        max_positions
    ):

        # =========================
        # NO REBALANCE
        # =========================
        if len(holdings) <= max_positions:

            return holdings

        # =========================
        # SCORE POSITIONS
        # =========================
        scored = []

        for code, pos in holdings.items():

            profit = pos.get(
                "profit",
                0
            )

            confidence = pos.get(
                "confidence",
                0
            )

            memory = self.rebalance_memory.get(
                code,
                0
            )

            score = (

                profit * 0.7 +

                confidence * 0.002 +

                memory * 0.3
            )
            if profit < 0:
                score -= 0.2


            scored.append(
                (
                    code,
                    pos,
                    score
                )
            )

        # =========================
        # SORT
        # =========================
        scored = sorted(
            scored,
            key=lambda x: x[2]
        )

        # =========================
        # REMOVE WEAKEST
        # =========================
        while len(scored) > max_positions:

            scored.pop(0)

        # =========================
        # REBUILD
        # =========================
        new_holdings = {}

        for code, pos, score in scored:

            new_holdings[code] = pos

        return new_holdings

    # =========================
    # UPDATE LEARNING
    # =========================
    def update_learning(
        self,
        code,
        pnl
    ):

        old = self.rebalance_memory.get(
            code,
            0
        )

        new = (
            old * 0.9 +
            pnl * 0.1
        )

        self.rebalance_memory[code] = new