     #core/portfolio/execution_engine.py

from core.portfolio.transaction_cost import TransactionCost
from core.portfolio.slippage import Slippage


class ExecutionEngine:

    def __init__(self):

        self.cost = TransactionCost()

        self.slippage = Slippage()

        # =========================
        # EXECUTION MEMORY
        # =========================
        self.execution_memory = {

            "buy_success": 0,
            "sell_success": 0,
            "buy_fail": 0
        }

    # =========================
    # BUY EXECUTE
    # =========================
    def buy(
        self,
        cash,
        price,
        shares,
        volatility=0
    ):

        # =========================
        # VOLATILITY SLIPPAGE
        # =========================
        exec_price = self.slippage.buy_price(
            price,
            volatility
        )

        fee = self.cost.cost(
            exec_price,
            shares
        )

        total = (
            exec_price * shares
        ) + fee

        # =========================
        # CASH CHECK
        # =========================
        if total > cash:

            self.execution_memory[
                "buy_fail"
            ] += 1

            return {
                "success": False
            }

        cash -= total

        self.execution_memory[
            "buy_success"
        ] += 1

        return {

            "success": True,

            "cash": cash,

            "price": exec_price,

            "fee": fee
        }

    # =========================
    # SELL EXECUTE
    # =========================
    def sell(
        self,
        cash,
        price,
        shares,
        volatility=0
    ):

        # =========================
        # VOLATILITY SLIPPAGE
        # =========================
        exec_price = self.slippage.sell_price(
            price,
            volatility
        )

        fee = self.cost.cost(
            exec_price,
            shares
        )

        total = (
            exec_price * shares
        ) - fee

        cash += total

        self.execution_memory[
            "sell_success"
        ] += 1

        return {

            "cash": cash,

            "price": exec_price,

            "fee": fee
        }

    # =========================
    # EXECUTION STATS
    # =========================
    def stats(self):

        return self.execution_memory