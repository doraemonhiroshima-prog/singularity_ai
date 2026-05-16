class Slippage:

    def __init__(self):

        # =========================
        # SLIPPAGE MEMORY
        # =========================
        self.slippage_memory = {

            "buy": [],
            "sell": []
        }

    # =========================
    # BUY PRICE
    # =========================
    def buy_price(
        self,
        price,
        volatility=0
    ):

        slip = 0.002

        # =========================
        # VOLATILITY ADJUST
        # =========================
        if volatility > 0.05:

            slip += 0.003

        elif volatility > 0.03:

            slip += 0.001

        exec_price = (
            price * (1 + slip)
        )

        # =========================
        # MEMORY
        # =========================
        self.slippage_memory[
            "buy"
        ].append(slip)

        return exec_price

    # =========================
    # SELL PRICE
    # =========================
    def sell_price(
        self,
        price,
        volatility=0
    ):

        slip = 0.002

        # =========================
        # VOLATILITY ADJUST
        # =========================
        if volatility > 0.05:

            slip += 0.003

        elif volatility > 0.03:

            slip += 0.001

        exec_price = (
            price * (1 - slip)
        )

        # =========================
        # MEMORY
        # =========================
        self.slippage_memory[
            "sell"
        ].append(slip)

        return exec_price

    # =========================
    # AVG SLIPPAGE
    # =========================
    def average_slippage(self):

        buy = self.slippage_memory["buy"]

        sell = self.slippage_memory["sell"]

        avg_buy = (
            sum(buy) / len(buy)
            if buy else 0
        )

        avg_sell = (
            sum(sell) / len(sell)
            if sell else 0
        )

        return {

            "buy": avg_buy,

            "sell": avg_sell
        }