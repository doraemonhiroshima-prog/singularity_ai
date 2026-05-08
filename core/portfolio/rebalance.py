class RebalanceManager:

    def rebalance(
        self,
        holdings,
        max_positions
    ):

        if len(holdings) <= max_positions:

            return holdings

        sorted_holdings = sorted(
            holdings.items(),
            key=lambda x: x[1].get(
                "profit",
                0
            )
        )

        while len(sorted_holdings) > max_positions:

            sorted_holdings.pop(0)

        return dict(sorted_holdings)