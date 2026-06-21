# core/investment/executor.py

class Executor:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(
        self,
        portfolio
    ):

        self.portfolio = portfolio

    # =====================================================
    # EXECUTE
    # =====================================================
    def execute(
        self,
        decisions,
        data_map
    ):

        for d in decisions:

            try:

                code = d["code"]

                if code not in data_map:

                    continue

                price = float(

                    data_map[code]["Close"]
                    .iloc[-1]

                )

                # =========================================
                # BUY
                # =========================================
                if d["action"] == "BUY":

                    self.portfolio.buy(

                        code,

                        price,

                        d["amount"]

                    )

                # =========================================
                # SELL ALL
                # =========================================
                elif d["action"] == "SELL_ALL":

                    self.portfolio.sell(

                        code,

                        price

                    )

                # =========================================
                # SELL HALF
                # =========================================
                elif d["action"] == "SELL_HALF":

                    self.portfolio.sell_partial(

                        code,

                        price,

                        0.5

                    )

                # =========================================
                # UPDATE PEAK
                # =========================================
                if code in self.portfolio.positions:

                    self.portfolio.update_peak(

                        code,

                        price

                    )

            except Exception as e:

                print(
                    "EXECUTOR ERROR:",
                    e
                )