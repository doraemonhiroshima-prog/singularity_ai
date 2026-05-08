import random

from ai.data_ai import DataAI
from ai.market_scan_ai import MarketScanAI
from ai.technical_ai import TechnicalAI
from ai.news_ai import NewsAI
from ai.future_prediction_ai import FuturePredictionAI
from ai.institution_ai import InstitutionAI

from ai.signal_ai import SignalAI
from ai.strategy_ai import StrategyAI
from ai.portfolio_ai import PortfolioAI


def run():

    # =========================
    # AI INITIALIZE
    # =========================
    data_ai = DataAI()

    market_ai = MarketScanAI()

    tech_ai = TechnicalAI()

    news_ai = NewsAI()

    inst_ai = InstitutionAI()

    future_ai = FuturePredictionAI()

    signal_ai = SignalAI()

    strategy_ai = StrategyAI()

    portfolio_ai = PortfolioAI(3000000)

    # =========================
    # LOAD DATA
    # =========================
    data_map = data_ai.load()

    if len(data_map) == 0:

        print("NO DATA")

        return

    print("DATA:", len(data_map))

    max_days = min([
        len(df)
        for df in data_map.values()
    ])

    print("MAX DAYS:", max_days)

    # =========================
    # PORTFOLIO
    # =========================
    cash = 3000000

    holdings = {}

    # =========================
    # MAIN LOOP
    # =========================
    for day in range(100, max_days):

        signal_count = 0

        buy_count = 0

        codes = list(data_map.keys())

        random.shuffle(codes)

        for code in codes[:300]:

            try:

                df = data_map[code].iloc[:day].copy()

                if len(df) < 60:
                    continue

                # =========================
                # AI ANALYSIS
                # =========================
                market = market_ai.run(df)

                tech = tech_ai.run(df)

                news = news_ai.run(code)

                inst = inst_ai.run(df)

                future = future_ai.run(df)

                # =========================
                # STRATEGY
                # =========================
                strategy = strategy_ai.build(df)

                regime = strategy["regime"]

                weights = strategy["weights"]

                threshold = strategy["threshold"]

                # =========================
                # SIGNAL
                # =========================
                signal = signal_ai.run(
                    {
                        "market": market,
                        "tech": tech,
                        "news": news,
                        "inst": inst,
                        "future": future
                    },
                    weights,
                    threshold
                )

                print(
                    f"{code} | "
                    f"{regime} | "
                    f"SCORE={round(signal['confidence'],2)} | "
                    f"TH={threshold} | "
                    f"{signal['signal']}"
                )

                if signal["signal"] != "BUY":

                    continue

                signal_count += 1

                # =========================
                # BUY
                # =========================
                price = float(
                    df["Close"].iloc[-1]
                )

                result = portfolio_ai.buy(
                    cash,
                    holdings,
                    code,
                    price,
                    signal["confidence"],
                    regime
                )

                cash = result["cash"]

                holdings = result["holdings"]

                if result["bought"]:

                    buy_count += 1

            except Exception as e:

                print("ERROR:", code, e)

                continue

        # =========================
        # TOTAL
        # =========================
        total = cash

        for code, pos in holdings.items():

            try:

                current_price = float(
                    data_map[code]["Close"].iloc[day]
                )

                total += (
                    pos["shares"] *
                    current_price
                )

            except:

                continue

        print(
            f"\nDAY {day} | "
            f"SIGNAL {signal_count} | "
            f"BUY {buy_count} | "
            f"TOTAL {int(total)}\n"
        )

    # =========================
    # FINAL
    # =========================
    final_total = cash

    for code, pos in holdings.items():

        try:

            final_price = float(
                data_map[code]["Close"].iloc[-1]
            )

            final_total += (
                pos["shares"] *
                final_price
            )

        except:

            continue

    print("\n=== RESULT ===")

    print("FINAL:", int(final_total))


if __name__ == "__main__":

    run()