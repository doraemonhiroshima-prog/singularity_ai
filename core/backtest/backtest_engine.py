class BacktestEngine:

    def __init__(self):

        self.logs = []

        self.equity_curve = []

        self.trade_count = 0

        self.win_count = 0

        self.loss_count = 0

        self.total_profit = 0

        self.total_loss = 0

    # =========================
    # BUY LOG
    # =========================
    def buy_log(
        self,
        day,
        code,
        shares,
        price
    ):

        self.logs.append({

            "type": "BUY",

            "day": day,

            "code": code,

            "shares": shares,

            "price": round(price, 2)
        })

    # =========================
    # SELL LOG
    # =========================
    def sell_log(
        self,
        day,
        code,
        shares,
        buy_price,
        sell_price
    ):

        profit = (
            sell_price - buy_price
        ) * shares

        pct = (
            (
                sell_price -
                buy_price
            ) / buy_price
        ) * 100

        self.trade_count += 1

        if profit > 0:

            self.win_count += 1

            self.total_profit += profit

        else:

            self.loss_count += 1

            self.total_loss += abs(profit)

        self.logs.append({

            "type": "SELL",

            "day": day,

            "code": code,

            "shares": shares,

            "buy": round(buy_price, 2),

            "sell": round(sell_price, 2),

            "profit": int(profit),

            "pct": round(pct, 2)
        })

    # =========================
    # EQUITY
    # =========================
    def update_equity(
        self,
        total
    ):

        self.equity_curve.append(total)

    # =========================
    # RESULT
    # =========================
    def result(self):

        winrate = 0

        if self.trade_count > 0:

            winrate = (
                self.win_count /
                self.trade_count
            ) * 100

        pf = 0

        if self.total_loss > 0:

            pf = (
                self.total_profit /
                self.total_loss
            )

        max_equity = 0

        max_dd = 0

        for v in self.equity_curve:

            if v > max_equity:

                max_equity = v

            dd = (
                max_equity - v
            ) / max_equity

            if dd > max_dd:

                max_dd = dd

        return {

            "trades": self.trade_count,

            "winrate": round(winrate, 2),

            "pf": round(pf, 2),

            "max_dd": round(max_dd * 100, 2)
        }

    # =========================
    # PRINT
    # =========================
    def print_logs(self):

        print("\n=== TRADE LOG ===")

        for log in self.logs[-30:]:

            print(log)