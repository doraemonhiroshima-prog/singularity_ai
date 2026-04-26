from investment.portfolio import Portfolio
from investment.portfolio_ai import PortfolioAI
from investment.executor import Executor
from investment.sell_ai import sell_signal
import investment.config as config

# 既存importはそのまま

class PipelineController:

    def __init__(self):

        self.market_ai = MarketScanAI()
        self.technical_ai = TechnicalAI()
        self.news_ai = NewsAI()
        self.inst_ai = InstitutionAI()

        # ★ 追加
        self.portfolio = Portfolio(config.INITIAL_CASH)
        self.portfolio_ai = PortfolioAI(config)
        self.executor = Executor(self.portfolio)

    def run(self):

        market_data = self.market_ai.process()
        tech_data = self.technical_ai.process(market_data)

        candidates = []

        data_map = {}

        for r in tech_data:

            news = self.news_ai.analyze(r["code"], r["name"])
            inst = self.inst_ai.analyze(r["df"])

            total = (
                r["market_score"] +
                r["technical_score"] +
                news["score"] +
                inst
            )

            candidates.append({
                "code": r["code"],
                "price": float(r["df"]["Close"].iloc[-1]),
                "score": total
            })

            data_map[r["code"]] = r["df"]

        # =========================
        # SELL
        # =========================
        sell_decisions = self.portfolio_ai.decide_sell(
            self.portfolio,
            data_map,
            sell_signal
        )

        self.executor.execute(sell_decisions, data_map)

        # =========================
        # BUY
        # =========================
        buy_decisions = self.portfolio_ai.decide_buy(
            candidates,
            self.portfolio
        )

        self.executor.execute(buy_decisions, data_map)

        print("CASH:", self.portfolio.cash)
        print("POSITIONS:", list(self.portfolio.positions.keys()))

        return candidates
