from core.portfolio.portfolio_ai import PortfolioAI as CorePortfolio


class PortfolioAI:

    def __init__(self, cash):

        self.core = CorePortfolio(cash)

    def buy(
        self,
        cash,
        holdings,
        code,
        price,
        confidence,
        regime
    ):

        return self.core.buy(
            cash,
            holdings,
            code,
            price,
            confidence,
            regime
        )