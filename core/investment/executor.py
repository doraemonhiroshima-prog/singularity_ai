class Executor:

    def __init__(self, portfolio):
        self.portfolio = portfolio

    def execute(self, decisions, data_map):

        for d in decisions:

            code = d["code"]

            if code not in data_map:
                continue

            price = float(data_map[code]["Close"].iloc[-1])

            if d["action"] == "BUY":
                self.portfolio.buy(code, price, d["amount"])

            elif d["action"] == "SELL_ALL":
                self.portfolio.sell(code, price)

            elif d["action"] == "SELL_HALF":
                self.portfolio.sell_partial(code, price, 0.5)

            # peak更新
            if code in self.portfolio.positions:
                self.portfolio.update_peak(code, price)
