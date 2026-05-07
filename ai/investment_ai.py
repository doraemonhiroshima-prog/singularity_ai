from core.portfolio.portfolio_ai import PortfolioAI

class InvestmentAI:

    def __init__(self, cash):
        self.core = PortfolioAI(cash)

    def buy(self, signal):
        self.core.buy(signal)

    def update(self, data_map, day):
        self.core.update(data_map, day)

    def total_value(self, data_map, day):
        return self.core.total_value(data_map, day)