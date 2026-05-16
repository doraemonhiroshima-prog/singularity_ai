class EntryManager:

    def position_size(self, cash, confidence, regime):

        size = 0.05

        # confidence
        if confidence >= 90:
            size += 0.20
        elif confidence >= 80:
            size += 0.15
        elif confidence >= 70:
            size += 0.10
        elif confidence >= 60:
            size += 0.05

        # regime
        if regime == "BULL":
            size += 0.05
        elif regime == "CRASH":
            size -= 0.05
        elif regime == "RANGE":
            size -= 0.02

        size = max(min(size, 0.30), 0.01)

        return cash * size

    def allow_entry(
        self,
        holdings,
        code,
        max_positions=10,
        confidence=0,
        signal_score=0,
        performance_memory=None
    ):

        if code in holdings:
            return False

        # =========================
        # AI MEMORY（勝ってる銘柄優先）
        # =========================
        memory_score = 0
        if performance_memory and code in performance_memory:
            memory_score = performance_memory[code]

        current_size = len(holdings)

        # 空きあり
        if current_size < max_positions * 0.8:
            return True

        # フル状態
        if current_size >= max_positions:

            return (
                signal_score >= 9 and
                confidence >= 80 and
                memory_score >= 0
            )

        # 中間
        return (
            signal_score >= 8 and
            confidence >= 70
        )