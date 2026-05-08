from core.portfolio.transaction_cost import TransactionCost
from core.portfolio.slippage import Slippage


class ExecutionEngine:

    def __init__(self):

        self.cost = TransactionCost()

        self.slippage = Slippage()

    # =========================
    # BUY EXECUTE
    # =========================
    def buy(
        self,
        cash,
        price,
        shares
    ):

        exec_price = self.slippage.buy_price(
            price
        )

        fee = self.cost.cost(
            exec_price,
            shares
        )

        total = (
            exec_price * shares
        ) + fee

        if total > cash:

            return {
                "success": False
            }

        cash -= total

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
        shares
    ):

        exec_price = self.slippage.sell_price(
            price
        )

        fee = self.cost.cost(
            exec_price,
            shares
        )

        total = (
            exec_price * shares
        ) - fee

        cash += total

        return {
            "cash": cash,
            "price": exec_price,
            "fee": fee
        }