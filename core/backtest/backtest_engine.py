import pandas as pd
from core.market_scan.pipeline_controller import PipelineController


class BacktestEngine:

    def __init__(self):
        self.controller = PipelineController()

        self.initial_cash = 3_000_000
        self.cash = self.initial_cash
        self.holdings = {}

        self.history = []

    # =========================
    # MAIN RUN
    # =========================
    def run(self, data_map):

        max_days = min(len(df) for df in data_map.values())

        for day in range(100, max_days):

            # =========================
            # SELL / BUY PIPELINE
            # =========================
            self.controller.portfolio = self._wrap_portfolio()

            result = self.controller.run()

            self.cash = self.controller.portfolio.cash
            self.holdings = self.controller.portfolio.positions

            # =========================
            # VALUATION
            # =========================
            total = self.cash

            for code, pos in self.holdings.items():

                price = data_map[code]["Close"].iloc[day]
                total += pos["shares"] * price

            self.history.append(total)

            print(f"DAY {day} TOTAL {int(total)}")

        return self.history

    # =========================
    # WRAP ADAPTER
    # =========================
    def _wrap_portfolio(self):

        class P:
            def __init__(self, cash, holdings):
                self.cash = cash
                self.positions = holdings

            def buy(self, code, price, amount):
                pass

            def sell(self, code, price):
                pass

            def sell_partial(self, code, price, ratio):
                pass

            def update_peak(self, code, price):
                pass

        return P(self.cash, self.holdings)