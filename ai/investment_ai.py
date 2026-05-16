from core.investment.executor import Executor
from core.investment.risk_manager import RiskManager
from core.investment.capital_allocator import CapitalAllocator


class InvestmentAI:

    def __init__(self, portfolio):

        self.portfolio = portfolio

        self.executor = Executor(portfolio)

        self.risk_manager = RiskManager()

        self.capital_allocator = CapitalAllocator()

    def execute(self, decisions, data_map):

        self.executor.execute(
            decisions,
            data_map
        )

    def allocate(self, cash, signals):

        return self.capital_allocator.allocate(
            cash,
            signals
        )

    def check_risk(self, signal):

        return self.risk_manager.check(
            self.portfolio,
            signal
        )