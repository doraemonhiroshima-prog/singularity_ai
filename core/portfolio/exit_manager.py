class ExitManager:

    def __init__(self):
        self.exit_memory = {}

    def update_learning(self, code, pnl):

        old = self.exit_memory.get(code, 0)

        new = old * 0.9 + pnl * 0.1

        self.exit_memory[code] = new

    def should_exit(self, df, entry_price, current_price, code=None, confidence=0):

        pnl = (current_price - entry_price) / entry_price

        memory = 0
        if code in self.exit_memory:
            memory = self.exit_memory[code]

        # =========================
        # 強制ホールド（勝ち株）
        # =========================
        if pnl > 0.40:
            return False, "MEGA_TREND_HOLD"

        if confidence >= 80 and pnl > 0.25:
            return False, "WINNER_HOLD"

        if pnl > 0.15 and memory > 0:
            return False, "MOMENTUM_HOLD"

        # =========================
        # STOP LOSS
        # =========================
        stop_loss = -0.10

        if confidence >= 85:
            stop_loss = -0.15

        if memory > 0:
            stop_loss -= 0.03

        if pnl <= stop_loss:
            return True, "STOP_LOSS"

        # =========================
        # TAKE PROFIT
        # =========================
        take_profit = 0.50

        if confidence >= 85:
            take_profit = 0.80

        if memory > 0:
            take_profit += 0.10

        if pnl >= take_profit:
            return True, "TAKE_PROFIT"

        # =========================
        # TRAILING STOP
        # =========================
        try:
            high20 = df["High"].rolling(20).max().iloc[-1]

            trailing = 0.88
            if memory > 0:
                trailing = 0.85

            if current_price < high20 * trailing:
                return True, "TRAILING_STOP"

        except:
            pass

        # =========================
        # TIME EXIT
        # =========================
        try:
            if len(df) > 20:

                recent = df["Close"].iloc[-10:].mean()

                if pnl < 0.03 and current_price < recent * 0.94:
                    return True, "TIME_EXIT"

        except:
            pass

        # =========================
        # VOLUME EXIT
        #=========================
        try:
            vol_now = df["Volume"].iloc[-1]
            vol_avg = df["Volume"].rolling(10).mean().iloc[-1]

            if pnl < -0.05:
                if vol_now < vol_avg * 0.25:
                    return True, "VOLUME_DROP"

        except:
            pass

        return False, ""