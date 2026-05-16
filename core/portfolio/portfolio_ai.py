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
        self.execution = ExecutionEngine()

        # memory
        self.memory = {}

    # =========================
    # EXIT（回転重視）
    # =========================
    def sell_check(self, holdings, code, df):

        if code not in holdings:
            return False, ""

        entry = holdings[code]["price"]
        current = float(df["Close"].iloc[-1])

        pnl = (current - entry) / entry

        # 利確（早め）
        if pnl >= 0.04:
            return True, "TAKE_PROFIT"

        # 損切り
        if pnl <= -0.04:
            return True, "STOP_LOSS"

        # =========================
        # 時間EXIT（超重要）
        # =========================
        try:
            if len(df) > 10:
                avg = df["Close"].iloc[-5:].mean()
                if current < avg * 0.985:
                    return True, "TIME_EXIT"
        except:
            pass

        return self.exit.should_exit(df, entry, current)

    # =========================
    # PRUNING（強制回転）
    # =========================
    def loss_pruning(self, holdings, prices):

        to_remove = []

        for code, pos in holdings.items():

            entry = pos["price"]
            current = prices.get(code, entry)

            pnl = (current - entry) / entry

            self.memory[code] = pnl

            # 即カット
            if pnl <= -0.05:
                to_remove.append(code)

        # =========================
        # 強制回転（重要）
        # =========================
        if len(holdings) > 8:

            sorted_pos = sorted(
                holdings.items(),
                key=lambda x: self.memory.get(x[0], 0)
            )

            remove_count = len(holdings) - 8

            for i in range(remove_count):
                to_remove.append(sorted_pos[i][0])

        for c in set(to_remove):
            if c in holdings:
                del holdings[c]

        return holdings

    # =========================
    # MEMORY UPDATE
    # =========================
    def update_memory(self, holdings, prices):

        for code, pos in holdings.items():

            entry = pos["price"]
            current = prices.get(code, entry)

            pnl = (current - entry) / entry

            self.memory[code] = pnl

    # =========================
    # BUY
    # =========================
    def buy(self, cash, holdings, code, price, confidence, regime, signal_score=0):

        max_positions = self.capital.max_positions(regime)

        allowed = self.entry.allow_entry(
            holdings,
            code,
            max_positions,
            confidence,
            signal_score,
            self.memory
        )

        if not allowed:
            return {"cash": cash, "holdings": holdings, "bought": False}

        cash_ratio = self.capital.cash_ratio(regime)
        usable_cash = cash * (1 - cash_ratio)

        penalty = 1 - max(0, -self.memory.get(code, 0))

        budget = self.entry.position_size(
            usable_cash * penalty,
            confidence,
            regime
        )

        shares = int(budget / price / 100) * 100

        if shares <= 0:
            return {"cash": cash, "holdings": holdings, "bought": False}

        result = self.execution.buy(cash, price, shares)

        if not result["success"]:
            return {"cash": cash, "holdings": holdings, "bought": False}

        holdings[code] = {
            "shares": shares,
            "price": result["price"],
            "profit": 0
        }

        return {
            "cash": result["cash"],
            "holdings": holdings,
            "bought": True
        }

    # =========================
    # EXEC SELL
    # =========================
    def execute_sell(self, cash, holdings, code, price):

        if code not in holdings:
            return {"cash": cash, "holdings": holdings, "sold": False}

        shares = holdings[code]["shares"]

        result = self.execution.sell(cash, price, shares)

        del holdings[code]

        return {
            "cash": result["cash"],
            "holdings": holdings,
            "sold": True
        }