   #core/portfolio/exit_manager.py

class ExitManager:

    def __init__(self):

        self.exit_memory = {}

        self.partial_taken = {}

    # ==================================================
    # LEARNING
    # ==================================================
    def update_learning(self, code, pnl):

        old = self.exit_memory.get(code, 0)

        self.exit_memory[code] = (
            old * 0.9 +
            pnl * 0.1
        )

    # ==================================================
    # EXIT
    # ==================================================
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

       
        
        memory = self.exit_memory.get(
            code,
            0
        )

        # =========================
        # HARD STOP
        # =========================
        hard_stop = -0.20

        

        if confidence >= 85:
            hard_stop = -0.15

        if pnl <= hard_stop:

            return True, "HARD_STOP"

        # =========================
        # SELL HALF
        # =========================
        if pnl >= 0.50:

            done = self.partial_taken.get(
                code,
                False
            )

            if not done:

                self.partial_taken[
                    code
                ] = True

                return True, "SELL_HALF"

        # =========================
        # WINNER HOLD
        # =========================
        if pnl >= 0.50:

            try:

                ma25 = (
                    df["Close"]
                    .rolling(25)
                    .mean()
                    .iloc[-1]
                )

                if current_price > ma25:

                    return False, "WINNER_HOLD"

            except:
                pass

        # =========================
        # SUPER TREND HOLD
        # =========================
        try:

            high20 = (
                df["High"]
                .rolling(20)
                .max()
                .iloc[-1]
            )

            vol_now = (
                df["Volume"]
                .iloc[-1]
            )

            vol_avg = (
                df["Volume"]
                .rolling(20)
                .mean()
                .iloc[-1]
            )

            if (

                current_price >
                high20 * 0.92

                and

                vol_now >
                vol_avg * 1.2

            ):

                return False, "SUPER_HOLD"

        except:
            pass

        # =========================
        # TRAILING STOP
        # =========================
        try:

            high50 = (
                df["High"]
                .rolling(50)
                .max()
                .iloc[-1]
            )

            trailing = 0.78

            if confidence >= 85:
                trailing = 0.72

            if current_price < (
                high50 * trailing
            ):

                return True, "TRAILING_STOP"

        except:
            pass

        # =========================
        # LOSER EXIT
        # =========================
        try:

            close = df["Close"]

            ma25 = (
                close
                .rolling(25)
                .mean()
                .iloc[-1]
            )

            if (

                pnl < 0

                and

                current_price < ma25

            ):

                return True, "MA25_BREAK"

        except:
            pass

       
        return False, ""