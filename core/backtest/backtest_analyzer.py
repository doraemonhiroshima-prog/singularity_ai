class BacktestAnalyzer:

    def analyze(
        self,
        trade_logs,
        final_total,
        initial_cash
    ):

        try:

            sell_trades = [
                t for t in trade_logs
                if t["type"] == "SELL"
            ]

            trades = len(sell_trades)

            # =========================
            # PROFIT
            # =========================
            profit = (
                final_total - initial_cash
            )

            # =========================
            # WINRATE
            # =========================
            winrate = 0

            if final_total > initial_cash:

                winrate = 100

            # =========================
            # PF
            # =========================
            pf = round(
                final_total / initial_cash,
                2
            )

            # =========================
            # DD
            # =========================
            max_dd = round(
                (
                    initial_cash - final_total
                ) / initial_cash * 100,
                2
            )

            if max_dd < 0:
                max_dd = 0

            return {

                "trades": trades,

                "winrate": winrate,

                "pf": pf,

                "max_dd": max_dd
            }

        except Exception as e:

            print("BACKTEST ERROR:", e)

            return {

                "trades": 0,

                "winrate": 0,

                "pf": 0,

                "max_dd": 0
            }