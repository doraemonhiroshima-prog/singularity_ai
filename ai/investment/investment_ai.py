from growth.growth_ai import GrowthAI


class InvestmentAI:

    def __init__(self, capital):
        self.cash = capital
        self.growth = GrowthAI()

    def decide(self, signals):

        trades = []
        weights = self.growth.get_weights()

        for s in signals:

            score = 0

            score += s["tech"] * weights["tech"] * 0.01
            score += s["inst"] * weights["inst"] * 0.02
            score += s["flow"] * weights["flow"] * 0.02
            score += s["news"] * weights["news"] * 0.05
            score += s["prob"] * weights["prob"] * 100

            # =========================
            # リスク制御
            # =========================
            if s["prob"] < 0.5:
                continue

            if score > 80:

                trades.append({
                    "type": "BUY",
                    "code": s["code"],
                    "price": s["price"],
                    "amount": 100000
                })

        return trades
