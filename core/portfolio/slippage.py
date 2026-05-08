class Slippage:

    def buy_price(
        self,
        price
    ):

        return price * 1.002

    def sell_price(
        self,
        price
    ):

        return price * 0.998