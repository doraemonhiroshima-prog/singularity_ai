class EntryManager:

    def position_size(
        self,
        cash,
        confidence,
        regime
    ):

        size = 0.05

        # =========================
        # CONFIDENCE
        # =========================
        if confidence >= 85:
            size += 0.15

        elif confidence >= 70:
            size += 0.10

        elif confidence >= 55:
            size += 0.05

        # =========================
        # REGIME
        # =========================
        if regime == "BULL":
            size += 0.05

        elif regime == "CRASH":
            size -= 0.03

        size = max(
            min(size, 0.25),
            0.02
        )

        return cash * size

    def allow_entry(
        self,
        holdings,
        code,
        max_positions=10
    ):

        if code in holdings:
            return False

        if len(holdings) >= max_positions:
            return False

        return True