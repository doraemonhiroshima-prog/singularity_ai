class TransactionCost:

    def cost(
        self,
        price,
        shares
    ):

        total = price * shares

        fee = total * 0.0015

        return fee