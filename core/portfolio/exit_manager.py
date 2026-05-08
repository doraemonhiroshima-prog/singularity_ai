class ExitManager:

    def should_exit(
        self,
        df,
        entry_price,
        current_price
    ):

        # =========================
        # STOP LOSS
        # =========================
        loss = (
            current_price - entry_price
        ) / entry_price

        if loss <= -0.08:

            return True, "STOP_LOSS"

        # =========================
        # TAKE PROFIT
        # =========================
        if loss >= 0.25:

            return True, "TAKE_PROFIT"

        # =========================
        # TRAILING STOP
        # =========================
        high20 = (
            df["High"]
            .rolling(20)
            .max()
            .iloc[-1]
        )

        if current_price < high20 * 0.90:

            return True, "TRAILING_STOP"

        # =========================
        # VOLUME EXIT
        # =========================
        vol_now = df["Volume"].iloc[-1]

        vol_avg = (
            df["Volume"]
            .rolling(10)
            .mean()
            .iloc[-1]
        )

        if vol_now < vol_avg * 0.5:

            return True, "VOLUME_DROP"

        # =========================
        # CLIMAX TOP
        # =========================
        if len(df) > 5:

            recent_gain = (
                current_price -
                df["Close"].iloc[-5]
            ) / df["Close"].iloc[-5]

            if recent_gain > 0.30:

                return True, "CLIMAX_TOP"

        return False, ""