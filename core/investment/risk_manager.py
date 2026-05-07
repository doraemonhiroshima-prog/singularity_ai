class RiskManager:

    def __init__(self):

        self.max_risk = 0.03
        self.max_positions = 5

    def check(self, portfolio, signal):

        if len(portfolio.positions) >= self.max_positions:
            return False

        if portfolio.cash <= 0:
            return False

        return True

    def position_size(self, portfolio, price):

        risk_cash = portfolio.cash * self.max_risk

        qty = int(risk_cash / price)

        return max(qty, 1)