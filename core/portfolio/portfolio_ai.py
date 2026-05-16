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

        # =========================
        # PERFORMANCE MEMORY
        # =========================
        self.memory = {}

        # =========================
        # GLOBAL STATS
        # =========================
        self.stats = {

            "wins": 0,
            "losses": 0,
            "total_trades": 0
        }

    # =========================
    # UPDATE MEMORY
    # =========================
    def update_memory(
        self,
        code,
        pnl
    ):

        old = self.memory.get(
            code,
            0
        )

        new = (
            old * 0.9 +
            pnl * 0.1
        )

        self.memory[code] = new

        # sub managers
        self.entry.update_learning(
            code,
            pnl
        )

        self.exit.update_learning(
            code,
            pnl
        )

        self.position.update_learning(
            code,
            pnl
        )

        self.rebalance.update_learning(
            code,
            pnl
        )

    # =========================
    # PRUNING
    # =========================
    def pruning(
        self,
        holdings,
        prices
    ):

        to_remove = []

        for code, pos in holdings.items():

            entry = pos["price"]

            current = prices.get(
                code,
                entry
            )

            pnl = (
                current - entry
            ) / entry

            # memory update
            self.update_memory(
                code,
                pnl
            )

            # =========================
            # HARD LOSS CUT
            # =========================
            if pnl <= -0.10:

                to_remove.append(code)

        # =========================
        # FORCE ROTATION
        # =========================
        if len(holdings) > 12:

            sorted_pos = sorted(

                holdings.items(),

                key=lambda x:
                self.memory.get(
                    x[0],
                    0
                )
            )

            remove_count = (
                len(holdings) - 12
            )

            for i in range(remove_count):

                to_remove.append(
                    sorted_pos[i][0]
                )

        # =========================
        # REMOVE
        # =========================
        for code in set(to_remove):

            if code in holdings:

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
        # MAX POSITIONS
        # =========================
        max_positions = (
            self.capital.max_positions(
                regime,
                confidence
            )
        )

        # =========================
        # ENTRY FILTER
        # =========================
        allowed = self.entry.allow_entry(

            holdings,

            code,

            max_positions,

            confidence,

            signal,

            self.memory
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
        cash_ratio = (
            self.capital.cash_ratio(
                regime,
                volatility
            )
        )

        usable_cash = (
            cash * (1 - cash_ratio)
        )

        # =========================
        # MEMORY BOOST
        # =========================
        memory = self.memory.get(
            code,
            0
        )

        if memory > 0:

            boost = (
                1 +
                min(memory, 0.30)
            )

        else:

            boost = (
                1 -
                min(abs(memory), 0.50)
            )

        # =========================
        # POSITION SIZE
        # =========================
        budget = (
            self.entry.position_size(

                usable_cash * boost,

                confidence,

                regime,

                memory,

                volatility
            )
        )

        # =========================
        # POSITION WEIGHT
        # =========================
        weight = (
            self.position.weight(
                confidence,
                memory
            )
        )

        budget *= weight

        # =========================
        # SHARES
        # =========================
        shares = int(
            budget / price / 100
        ) * 100

        if shares <= 0:

            return {

                "cash": cash,

                "holdings": holdings,

                "bought": False
            }

        # =========================
        # EXECUTION
        # =========================
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

        # =========================
        # POSITION CREATE
        # =========================
        holdings[code] = {

            "shares": shares,

            "price": result["price"],

            "profit": 0,

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
    def sell_check(
        self,
        holdings,
        code,
        df
    ):

        if code not in holdings:

            return False, ""

        try:

            entry = holdings[code]["price"]

            current = float(
                df["Close"].iloc[-1]
            )

            confidence = holdings[
                code
            ].get(
                "confidence",
                0
            )

            pnl = (
                current - entry
            ) / entry

            # =========================
            # MEMORY UPDATE
            # =========================
            self.update_memory(
                code,
                pnl
            )

            # =========================
            # BIG WIN HOLD
            # =========================
            if pnl >= 1.20:

                return False, ""

            # =========================
            # EXIT ENGINE
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
    # EXECUTE SELL
    # =========================
    def execute_sell(
        self,
        cash,
        holdings,
        code,
        current_price,
        volatility=0
    ):

        if code not in holdings:

            return {

                "cash": cash,

                "holdings": holdings,

                "sold": False
            }

        try:

            shares = holdings[
                code
            ]["shares"]

            entry = holdings[
                code
            ]["price"]

            pnl = (
                current_price - entry
            ) / entry

            # =========================
            # STATS
            # =========================
            self.stats[
                "total_trades"
            ] += 1

            if pnl > 0:

                self.stats[
                    "wins"
                ] += 1

            else:

                self.stats[
                    "losses"
                ] += 1

            # =========================
            # MEMORY UPDATE
            # =========================
            self.update_memory(
                code,
                pnl
            )

            # =========================
            # EXECUTION
            # =========================
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

        total = self.stats[
            "total_trades"
        ]

        if total == 0:

            return 0

        return (
            self.stats["wins"] /
            total
        )