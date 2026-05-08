from core.portfolio.entry_manager import EntryManager
from core.portfolio.exit_manager import ExitManager
from core.portfolio.position_manager import PositionManager
from core.portfolio.capital_manager import CapitalManager
from core.portfolio.rebalance import RebalanceManager
from core.portfolio.execution_engine import ExecutionEngine

class PortfolioAI:

    def __init__(self, cash):

        self.initial_cash = cash

        self.entry = EntryManager()

        self.exit = ExitManager()

        self.position = PositionManager()

        self.capital = CapitalManager()

        self.rebalance = RebalanceManager()

    # =========================
    # BUY
    # =========================
    def buy(
        self,
        cash,
        holdings,
        code,
        price,
        confidence,
        regime
    ):

        max_positions = (
            self.capital.max_positions(
                regime
            )
        )

        allowed = self.entry.allow_entry(
            holdings,
            code,
            max_positions
        )

        if not allowed:

            return {
                "cash": cash,
                "holdings": holdings,
                "bought": False
            }

        budget = self.entry.position_size(
            cash,
            confidence,
            regime
        )

        shares = int(budget / price / 100) * 100

        if shares <= 100:

            return {
                "cash": cash,
                "holdings": holdings,
                "bought": False
            }

        cost = shares * price

        if cost > cash:

            return {
                "cash": cash,
                "holdings": holdings,
                "bought": False
            }

        style = self.position.style(
            regime,
            confidence
        )

        holdings[code] = {
            "shares": shares,
            "price": price,
            "style": style,
            "profit": 0
        }

        cash -= cost

        holdings = self.rebalance.rebalance(
            holdings,
            max_positions
        )

        return {
            "cash": cash,
            "holdings": holdings,
            "bought": True
        }

    # =========================
    # SELL
    # =========================
    def sell_check(
        self,
        holdings,
        code,
        df
    ):

        if code not in holdings:

            return False, ""

        entry = holdings[code]["price"]

        current = df["Close"].iloc[-1]

        return self.exit.should_exit(
            df,
            entry,
            current
        )