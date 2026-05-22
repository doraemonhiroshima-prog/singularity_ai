from core.portfolio.entry_manager import EntryManager
from core.portfolio.exit_manager import ExitManager
from core.portfolio.position_manager import PositionManager
from core.portfolio.capital_manager import CapitalManager
from core.portfolio.rebalance import RebalanceManager
from core.portfolio.execution_engine import ExecutionEngine
from core.portfolio.exit_manager import ExitManager

class PortfolioAI:

    def __init__(self, cash):

        self.initial_cash = cash
        
        self.entry = EntryManager()
        self.exit = ExitManager()
        self.position = PositionManager()
        self.capital = CapitalManager()
        self.rebalance = RebalanceManager()
        self.execution = ExecutionEngine()
        self.exit = ExitManager()
        self.memory = {}

        self.stats = {
            "wins": 0,
            "losses": 0,
            "total_trades": 0
        }

        # =========================
        # RISK STATE
        # =========================
        self.peak_value = cash
        self.current_dd = 0.0

    # =========================
    # DD UPDATE
    # =========================
    def update_dd(self, total_value):

        if total_value > self.peak_value:
            self.peak_value = total_value

        self.current_dd = (
            total_value - self.peak_value
        ) / self.peak_value

        # DDをキャピタルに反映
        self.capital.update_dd(self.current_dd)

        return self.current_dd

    # =========================
    # MEMORY UPDATE
    # =========================
    def update_memory(self, code, pnl):

        old = self.memory.get(code, 0)

        new = old * 0.9 + pnl * 0.1

        self.memory[code] = new

        self.entry.update_learning(code, pnl)
        self.exit.update_learning(code, pnl)
        self.position.update_learning(code, pnl)
        self.rebalance.update_learning(code, pnl)

    # =========================
    # PRUNING（重要）
    # =========================
    def prune(self, holdings, max_positions):

        if len(holdings) > max_positions * 1.2:
            return holdings

        # 弱い順に削除
        sorted_pos = sorted(
            holdings.items(),
            key=lambda x: self.memory.get(x[0], 0)
        )

        remove_count = len(holdings) - max_positions

        for i in range(remove_count):
            code = sorted_pos[i][0]
            del holdings[code]

        return holdings

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
        regime,
        signal,
        volatility=0
    ):

        # =========================
        # DD更新
        # =========================
        max_positions = self.capital.max_positions(regime, confidence)

        # ★ 強制整理
        holdings = self.prune(holdings, int(max_positions * 0.9))

        # =========================
        # ENTRY CHECK
        # =========================
        allowed = self.entry.allow_entry(
            holdings, code, max_positions, confidence, signal, self.memory, regime
        )

        if not allowed:
            return {
                "cash": cash,
                "holdings": holdings,
                "bought": False
            }

        # =========================
        # CASH CONTROL
        # =========================
        cash_ratio = self.capital.cash_ratio(regime, volatility)
        usable_cash = cash * (1 - cash_ratio)

        memory = self.memory.get(code, 0)

        boost = (
            1 + min(memory, 0.30)
            if memory > 0
            else 1 - min(abs(memory), 0.50)
        )

        budget = self.entry.position_size(
            usable_cash * boost,
            confidence,
            regime,
            memory,
            volatility
        )

        weight = self.position.weight(confidence, memory)

        budget *= weight

        shares = int(budget / price / 100) * 100

        if shares <= 0:
            return {
                "cash": cash,
                "holdings": holdings,
                "bought": False
            }

        result = self.execution.buy(
            cash,
            price,
            shares,
            volatility
        )

        if not result["success"]:
            return {
                "cash": cash,
                "holdings": holdings,
                "bought": False
            }

        holdings[code] = {
            "shares": shares,
            "price": result["price"],
            "confidence": confidence,
            "regime": regime
        }

        return {
            "cash": result["cash"],
            "holdings": holdings,
            "bought": True
        }

    # =========================
    # SELL CHECK
    # =========================
    def sell_check(self, holdings, code, df):

        if code not in holdings:
            return False, ""

        try:
            entry = holdings[code]["price"]
            current = float(df["Close"].iloc[-1])

            confidence = holdings[code].get("confidence", 0)

            pnl = (current - entry) / entry

            self.update_memory(code, pnl)

            # =========================
            # 強制利確フィルター
            # =========================
            if pnl >= 1.50:
                return False, ""

            # =========================
            # EXIT
            # =========================
            return self.exit.should_exit(
                df,
                entry,
                current,
                code,
                confidence
            )

        except:
            return False, ""

    # =========================
    # SELL EXECUTION
    # =========================
    def execute_sell(self, cash, holdings, code, current_price, volatility=0):

        if code not in holdings:
            return {
                "cash": cash,
                "holdings": holdings,
                "sold": False
            }

        try:
            shares = holdings[code]["shares"]
            entry = holdings[code]["price"]

            pnl = (current_price - entry) / entry

            self.stats["total_trades"] += 1

            if pnl > 0:
                self.stats["wins"] += 1
            else:
                self.stats["losses"] += 1

            self.update_memory(code, pnl)

            result = self.execution.sell(
                cash,
                current_price,
                shares,
                volatility
            )

            del holdings[code]

            return {
                "cash": result["cash"],
                "holdings": holdings,
                "sold": True
            }

        except:
            return {
                "cash": cash,
                "holdings": holdings,
                "sold": False
            }

    # =========================
    # WIN RATE
    # =========================
    def win_rate(self):

        t = self.stats["total_trades"]

        if t == 0:
            return 0

        return self.stats["wins"] / t