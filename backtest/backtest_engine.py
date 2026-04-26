import pandas as pd


class BacktestEngine:

    def __init__(self, initial_cash=1_000_000):
        self.cash = initial_cash
        self.position = 0
        self.entry_price = 0
        self.history = []

    def run(self, df, signal_func, strategy_func):

        for i in range(50, len(df)):  # 初期バー確保
            window = df.iloc[:i]

            price = float(df["Close"].iloc[i])

            # =========================
            # シグナル生成
            # =========================
            signal_data = signal_func(window)

            # =========================
            # 戦略判断
            # =========================
            decision = strategy_func(signal_data, price)

            action = decision.get("action", "HOLD")

            # =========================
            # BUY
            # =========================
            if action == "BUY" and self.position == 0:

                size = decision.get("size", 1.0)
                invest = self.cash * size

                self.position = invest / price
                self.entry_price = price
                self.cash -= invest

            # =========================
            # SELL
            # =========================
            elif action == "SELL" and self.position > 0:

                self.cash += self.position * price
                self.position = 0
                self.entry_price = 0

            # =========================
            # 損切り / 利確
            # =========================
            elif self.position > 0:

                stop = decision.get("stop_loss", 0)
                take = decision.get("take_profit", 999999)

                if price <= stop or price >= take:
                    self.cash += self.position * price
                    self.position = 0
                    self.entry_price = 0

            # =========================
            # 記録
            # =========================
            total = self.cash + self.position * price

            self.history.append({
                "time": df.index[i],
                "price": price,
                "total": total
            })

        return pd.DataFrame(self.history)
