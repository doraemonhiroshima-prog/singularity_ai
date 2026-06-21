# core/investment/sell_ai.py

from core.investment import config


def sell_signal(

    df,

    buy_price,

    peak_price=None
):

    try:

        current_price = float(
            df["Close"].iloc[-1]
        )

        # =========================================
        # SMA
        # =========================================
        sma5 = float(

            df["Close"]
            .rolling(5)
            .mean()
            .iloc[-1]
        )

        sma25 = float(

            df["Close"]
            .rolling(25)
            .mean()
            .iloc[-1]
        )

        # =========================================
        # PROFIT
        # =========================================
        change = (

            current_price -
            buy_price

        ) / buy_price

        # =========================================
        # TAKE PROFIT
        # =========================================
        if change >= config.TAKE_PROFIT:

            return "TAKE_PROFIT"

        # =========================================
        # STOP LOSS
        # =========================================
        if change <= config.STOP_LOSS:

            return "STOP_LOSS"

        # =========================================
        # TREND BREAK
        # =========================================
        if (

            sma5 < sma25 and
            current_price < sma25

        ):

            return "TREND_BREAK"

        # =========================================
        # TRAILING
        # =========================================
        if peak_price is not None:

            if current_price < (

                peak_price *

                (
                    1 -
                    config.TRAILING_STOP
                )

            ):

                return "TRAILING_STOP"

        # =========================================
        # HOLD
        # =========================================
        return "HOLD"

    except Exception as e:

        print(
            f"SELL ERROR: {e}"
        )

        return "HOLD"