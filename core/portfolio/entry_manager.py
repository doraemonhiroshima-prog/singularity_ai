class EntryManager:

    def __init__(self):

        # =========================
        # ENTRY LEARNING
        # =========================
        self.entry_memory = {}

    # =========================
    # POSITION SIZE
    # =========================
    def position_size(
        self,
        cash,
        confidence,
        regime,
        memory_score=0,
        volatility=0
    ):

        base = 0.05

        # =========================
        # CONFIDENCE BOOST
        # =========================
        if confidence >= 90:

            base += 0.25

        elif confidence >= 80:

            base += 0.22

        elif confidence >= 70:

            base += 0.12

        elif confidence >= 55:

            base += 0.06

        # =========================
        # REGIME ADJUSTMENT
        # =========================
        if regime == "BULL":

            base += 0.05

        elif regime == "CRASH":

            base -= 0.04

        elif regime == "RANGE":

            base -= 0.02

        # =========================
        # MEMORY BOOST
        # =========================
        if memory_score > 0:

            base += min(
                memory_score * 0.10,
                0.10
            )

        # =========================
        # VOLATILITY CONTROL
        # =========================
        if volatility > 0.05:

            base -= 0.05

        elif volatility > 0.03:

            base -= 0.02

        # =========================
        # LIMIT
        # =========================
        base = max(
            min(base, 0.30),
            0.02
        )

        return cash * base

    # =========================
    # ALLOW ENTRY
    # =========================
    def allow_entry(
        self,
        holdings,
        code,
        max_positions=10,
        confidence=0,
        signal_score=0,
        performance_memory=None
    ):

        # =========================
        # ALREADY HOLDING
        # =========================
        if code in holdings:

            return False

        size = len(holdings)

        # =========================
        # MEMORY
        # =========================
        memory_score = 0

        if (
            performance_memory and
            code in performance_memory
        ):

            memory_score = (
                performance_memory[code]
            )

        # =========================
        # FREE SPACE
        # =========================
        if size < max_positions * 0.7:

            return True

        # =========================
        # FULL PORTFOLIO
        # =========================
        if size >= max_positions:

            return (

                signal_score >= 6 and
                confidence >= 75 and
                memory_score >= -0.05
            )

        # =========================
        # MID ZONE
        # =========================
        return (

            signal_score >= 7 and
            confidence >= 60
        )

    # =========================
    # LEARNING UPDATE
    # =========================
    def update_learning(
        self,
        code,
        pnl
    ):

        old = self.entry_memory.get(
            code,
            0
        )

        new = (
            old * 0.9 +
            pnl * 0.1
        )

        self.entry_memory[code] = new