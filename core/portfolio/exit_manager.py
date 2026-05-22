class ExitManager:

    def __init__(self):
        self.exit_memory = {}

    # =========================
    # LEARNING
    # =========================
    def update_learning(self, code, pnl):

        old = self.exit_memory.get(code, 0)

        new = old * 0.9 + pnl * 0.1

        self.exit_memory[code] = new

    # =========================
    # MAIN EXIT LOGIC
    # =========================
    def should_exit(
        self,
        df,
        entry_price,
        current_price,
        code=None,
        confidence=0
    ):

        pnl = (
            current_price - entry_price
        ) / entry_price

        memory = self.exit_memory.get(code, 0)

        # =========================================================
        # ① HARD STOP
        # =========================================================
        hard_stop = -0.20

        if confidence >= 85:
            hard_stop = -0.15

        if memory < -0.10:
            hard_stop -= 0.02

        if pnl <= hard_stop:
            return True, "HARD_STOP"

        # =========================================================
        # ② VOLUME DRY
        # =========================================================
        try:

            vol_now = df["Volume"].iloc[-1]

            vol_avg = (
                df["Volume"]
                .rolling(10)
                .mean()
                .iloc[-1]
            )

            if pnl < 0:

                if vol_now < vol_avg * 0.3:
                    return True, "VOLUME_DRY_EXIT"

        except:
            pass

        # =========================================================
        # ③ SHORT TREND BREAK
        # =========================================================
        try:

            close = df["Close"]

            if len(close) > 5:

                if close.iloc[-1] < close.iloc[-3]:

                    if pnl < 0.05:
                        return True, "SHORT_TREND_BREAK"

        except:
            pass

        # =========================================================
        # ④ SUPER TREND HOLD
        # =========================================================
        try:

            if confidence >= 85 and pnl >= 0.20:

                high20 = (
                    df["High"]
                    .rolling(20)
                    .max()
                    .iloc[-1]
                )

                vol_now = df["Volume"].iloc[-1]

                vol_avg = (
                    df["Volume"]
                    .rolling(20)
                    .mean()
                    .iloc[-1]
                )

                # 高値維持 + 出来高維持
                if (
                    current_price >= high20 * 0.92 and
                    vol_now >= vol_avg * 1.2
                ):
                    return False, "SUPER_TREND_HOLD"

        except:
            pass

        # =========================================================
        # ⑤ TAKE PROFIT
        # =========================================================
        if pnl >= 0.35:
            return True, "TAKE_PROFIT_1"

        if pnl >= 0.60 and confidence < 85:
            return True, "TAKE_PROFIT_2"

        # =========================================================
        # ⑥ WINNER HOLD
        # =========================================================
        if pnl >= 0.50:
            return False, "WINNER_HOLD"

        if confidence >= 85 and pnl >= 0.30:
            return False, "STRONG_HOLD"

        if pnl >= 0.15 and memory > 0:
            return False, "MOMENTUM_HOLD"

        # =========================================================
        # ⑦ TRAILING STOP
        # =========================================================
        try:

            high20 = (
                df["High"]
                .rolling(20)
                .max()
                .iloc[-1]
            )

            trailing = 0.85

            # 強銘柄は粘る
            if confidence >= 80:
                trailing = 0.83

            # 弱銘柄は逃げる
            if memory < 0:
                trailing = 0.90

            # 含み損だけ早逃げ
            if pnl < -0.05:
                trailing += 0.01

            if current_price < high20 * trailing:
                return True, "TRAILING_STOP"

        except:
            pass

        # =========================================================
        # ⑧ TIME DECAY
        # =========================================================
        try:

            if len(df) > 20:

                recent = (
                    df["Close"]
                    .iloc[-10:]
                    .mean()
                )

                if (
                    pnl < 0.03 and
                    current_price < recent * 0.94
                ):
                    return True, "TIME_DECAY_EXIT"

        except:
            pass

        # =========================================================
        # ⑨ HOLD
        # =========================================================
        return False, ""