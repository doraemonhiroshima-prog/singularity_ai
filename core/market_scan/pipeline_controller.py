class PipelineController:

    def __init__(self):

        self.market_ai = MarketScanAI()
        self.technical_ai = TechnicalAI()
        self.news_ai = NewsAI()
        self.inst_ai = InstitutionAI()

        from core.investment.executor import Executor
        from core.investment.sell_ai import sell_signal
        import core.investment.config as config

        self.portfolio = None
        self.portfolio_ai = PortfolioAI(config)
        self.executor = None

    def run(self):

        if self.portfolio is None:
            return []

        market_data = self.market_ai.process()
        tech_data = self.technical_ai.process(market_data)

        candidates = []
        data_map = {}

        for r in tech_data:

            df = r["df"]

            total = (
                r["market_score"] +
                r["technical_score"]
            )

            candidates.append({
                "code": r["code"],
                "price": float(df["Close"].iloc[-1]),
                "score": total
            })

            data_map[r["code"]] = df

        # SELL
        sell = self.portfolio_ai.decide_sell(
            self.portfolio,
            data_map,
            sell_signal
        )

        self.executor.execute(sell, data_map)

        # BUY
        buy = self.portfolio_ai.decide_buy(
            candidates,
            self.portfolio
        )

        self.executor.execute(buy, data_map)

        return candidates