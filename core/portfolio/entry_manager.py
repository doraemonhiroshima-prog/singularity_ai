   #core/portfolio/entry_manager.py


class EntryManager:

    def __init__(self):
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

        if confidence >= 90:
            base += 0.25
        elif confidence >= 80:
            base += 0.10
        elif confidence >= 70:
            base += 0.07
        elif confidence >= 55:
            base += 0.03

        if regime == "BULL":
            base += 0.05
        elif regime == "CRASH":
            base -= 0.04
        elif regime == "RANGE":
            base -= 0.02

        if memory_score > 0:
            base += min(memory_score * 0.10, 0.10)

        if volatility > 0.05:
            base -= 0.05
        elif volatility > 0.03:
            base -= 0.02

        base = max(min(base, 0.15), 0.02)

        return cash * base

    # =========================
    # ENTRY CHECK（整理版）
    # =========================
    def allow_entry(
        self,
        holdings,
        code,
        max_positions,
        confidence,
        signal_score,
        performance_memory,
        regime
    ):

        if code in holdings:
            return False

        size = len(holdings)

        memory_score = 0
        if performance_memory and code in performance_memory:
            memory_score = performance_memory[code]

        # =========================
        # ① ENTRY ZONE（余裕あり）
        # =========================
        if size < max_positions * 1.00:
            return True
        # =========================
        # ② NORMAL ZONE（通常制御）
        # =========================
        if size < max_positions:
            return (
                signal_score >= 3 and
                confidence >= 50
            )

        # =========================
        # ③ OVER LIMIT（厳格フィルター）
        # =========================
        return (
            signal_score >= 6 and
            confidence >= 60 and
            memory_score >= 0
        )

    # =========================
    # LEARNING
    # =========================
    def update_learning(self, code, pnl):

        old = self.entry_memory.get(code, 0)
        self.entry_memory[code] = old * 0.9 + pnl * 0.1