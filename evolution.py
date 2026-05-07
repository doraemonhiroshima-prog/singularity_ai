import pandas as pd

from ai.data_ai import DataAI
from ai.market_scan_ai import MarketScanAI
from ai.technical_ai import TechnicalAI
from ai.news_ai import NewsAI
from ai.future_prediction_ai import FuturePredictionAI

from core.institution.institution_ai import InstitutionAI

from core.strategy.scorer import Scorer
from core.signal.signals import SignalGenerator
from core.strategy.strategy import StrategyAI

from core.investment.portfolio_ai import PortfolioAI
from core.investment.risk_manager import RiskManager
from core.investment.capital_allocator import CapitalAllocator


START_CASH = 3000000


def run():

    data_ai = DataAI()

    market_ai = MarketScanAI()
    technical_ai = TechnicalAI()
    news_ai = NewsAI()
    institution_ai = InstitutionAI()
    future_ai = FuturePredictionAI()

    scorer = Scorer()

    signal_ai = SignalGenerator()
    strategy_ai = StrategyAI()

    portfolio = PortfolioAI(START_CASH)

    risk_manager = RiskManager()
    allocator = CapitalAllocator()

    data_map = data_ai.load()

    print("DATA:", len(data_map))

    if len(data_map) == 0:
        return

    max_days = min([len(df) for df in data_map.values()])

    print("MAX DAYS:", max_days)

    for day in range(100, max_days):

        signals = []

        market_data = market_ai.run(data_map, day)

        market_score = market_data.get("score", 50)

        for code, df in data_map.items():

            try:

                if day >= len(df):
                    continue

                past = df.iloc[:day]

                price = float(df.iloc[day]["Close"])

                technical = technical_ai.run(past)["score"]

                news = news_ai.run(code)["score"]

                institution = institution_ai.run(past)["score"]

                future = future_ai.run(past)["score"]

                score = scorer.calculate({
                    "technical": technical,
                    "institution": institution,
                    "news": news,
                    "future": future,
                    "market": market_score
                })

                signal = signal_ai.generate({
                    "future": future,
                    "tech": technical,
                    "inst": institution
                })

                if signal["signal"] != "BUY":
                    continue

                signals.append({
                    "code": code,
                    "price": price,
                    "score": score
                })

            except:
                continue

        signals = sorted(
            signals,
            key=lambda x: x["score"],
            reverse=True
        )

        selected = strategy_ai.select(signals)

        selected = allocator.allocate(
            portfolio.cash,
            selected
        )

        buy_count = 0

        for signal in selected:

            if not risk_manager.check(
                portfolio,
                signal
            ):
                continue

            qty = risk_manager.position_size(
                portfolio,
                signal["price"]
            )

            signal["qty"] = qty

            portfolio.buy(signal)

            buy_count += 1

        portfolio.update(data_map, day)

        print(
            f"DAY {day} | "
            f"SIGNAL {len(signals)} | "
            f"BUY {buy_count}"
        )

    final = portfolio.total_value(
        data_map,
        max_days - 1
    )

    print("\n=== RESULT ===")
    print("FINAL:", int(final))


if __name__ == "__main__":
    run()