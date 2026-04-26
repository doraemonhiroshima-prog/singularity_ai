class Portfolio:

    def __init__(self, cash):
        self.cash = cash
        self.positions = {}

    # =========================
    # BUY
    # =========================
    def buy(self, code, price, amount):

        if price <= 0:
            return

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

    # =========================
    # SELL（全売却）
    # =========================
    def sell(self, code, price):

        if code not in self.positions:
            return

        pos = self.positions[code]
        shares = pos["shares"]

        self.cash += shares * price

        del self.positions[code]

    # =========================
    # 部分売却
    # =========================
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

    # =========================
    # 高値更新（トレーリング用）
    # =========================
    def update_peak(self, code, price):

        if code in self.positions:
            if price > self.positions[code]["peak"]:
                self.positions[code]["peak"] = price

    # =========================
    # 評価額
    # =========================
    def get_value(self, price_dict):

        total = self.cash

        for code, pos in self.positions.items():
            if code in price_dict:
                total += pos["shares"] * price_dict[code]

        return total

    # =========================
    # 状態表示
    # =========================
    def summary(self):

        print("\n===== PORTFOLIO =====")
        print(f"Cash: {self.cash:.0f}")

        for code, pos in self.positions.items():
            print(
                f"{code} | "
                f"{pos['shares']}株 | "
                f"買値:{pos['buy_price']:.2f} | "
                f"高値:{pos['peak']:.2f}"
            )

        print("=====================\n")
