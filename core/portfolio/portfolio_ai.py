import json


class PortfolioAI:

    def __init__(self, cash):
        self.cash = cash
        self.positions = {}

        try:
            with open("config.json", "r") as f:
                self.config = json.load(f)
        except:
            self.config = {}

    def buy(self, signal):

        code = signal["code"]
        price = signal["price"]

        if code in self.positions:
            return

        max_pos = self.config.get("max_positions", 5)

        if len(self.positions) >= max_pos:
            return

        risk = self.config.get("risk_per_trade", 0.05)
        size = self.cash * risk

        qty = int(size / price)

        if qty <= 0:
            return

        self.cash -= qty * price

        self.positions[code] = {
            "price": price,
            "qty": qty,
            "max_price": price
        }

    def update(self, data_map, day):

        tp = self.config.get("take_profit", 1.1)
        sl = self.config.get("stop_loss", 0.93)
        ts = self.config.get("trailing_stop", 0.03)

        for code, pos in list(self.positions.items()):

            if code not in data_map:
                continue

            df = data_map[code]

            if day >= len(df):
                continue

            price = df.iloc[day]["Close"]

            if price > pos["max_price"]:
                pos["max_price"] = price

            entry = pos["price"]

            if price >= entry * tp:
                self.sell(code, price)
                continue

            if price <= entry * sl:
                self.sell(code, price)
                continue

            drop = (pos["max_price"] - price) / pos["max_price"]

            if drop >= ts:
                self.sell(code, price)
                continue

    def sell(self, code, price):

        pos = self.positions[code]

        qty = pos["qty"]
        self.cash += qty * price

        del self.positions[code]

    def total_value(self, data_map, day):

        total = self.cash

        for code, pos in self.positions.items():

            if code not in data_map:
                continue

            df = data_map[code]

            if day >= len(df):
                continue

            price = df.iloc[day]["Close"]
            total += price * pos["qty"]

        return total