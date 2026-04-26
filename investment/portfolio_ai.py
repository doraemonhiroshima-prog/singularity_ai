class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.positions = {}

    def buy(self, code, price, amount):
        shares = int(amount / price)

        if shares <= 0:
            return

        cost = shares * price

        if cost > self.cash:
            return

        self.cash -= cost

        self.positions[code] = {
            "shares": shares,
            "buy_price": price,
            "peak": price,
            "half_sold": False
        }

    def sell(self, code, price):
        if code not in self.positions:
            return

        pos = self.positions[code]
        shares = pos["shares"]

        self.cash += shares * price
        del self.positions[code]

    def sell_partial(self, code, price, ratio):
        if code not in self.positions:
            return

        pos = self.positions[code]
        sell_shares = int(pos["shares"] * ratio)

        if sell_shares <= 0:
            return

        self.cash += sell_shares * price
        pos["shares"] -= sell_shares

        if pos["shares"] <= 0:
            del self.positions[code]

    def update_peak(self, code, price):
        if code in self.positions:
            if price > self.positions[code]["peak"]:
                self.positions[code]["peak"] = price
