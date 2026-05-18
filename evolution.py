import random
import traceback

from ai.data_ai import DataAI
from ai.market_scan_ai import MarketScanAI
from ai.technical_ai import TechnicalAI
from ai.news_ai import NewsAI
from ai.future_prediction_ai import FuturePredictionAI
from ai.institution_ai import InstitutionAI

from ai.signal_ai import SignalAI
from ai.strategy_ai import StrategyAI

import ai.portfolio_ai as p
import random
import numpy as np

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

PortfolioAI = p.PortfolioAI

print("USING:", p.__file__)


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

    portfolio_ai = PortfolioAI(
        3000000
    )

    # =========================
    # LOAD DATA
    # =========================
    data_map = data_ai.load()

    if len(data_map) == 0:

        print("NO DATA")

        return

    print("DATA:", len(data_map))

    # =========================
    # MAX DAYS
    # =========================
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

        hold_count = len(holdings)

        # =========================
        # RANDOM SCAN
        # =========================
        codes = list(data_map.keys())

        random.shuffle(codes)

        # 高速化
        scan_codes = codes[:100]

        # =========================
        # SELL CHECK
        # =========================
        sell_codes = []

        for code, pos in list(holdings.items()):

            try:

                df = (
                    data_map[code]
                    .iloc[:day]
                    .copy()
                )

                should_sell, reason = (
                    portfolio_ai.sell_check(
                        holdings,
                        code,
                        df
                    )
                )

                if should_sell:

                    current_price = float(
                        df["Close"].iloc[-1]
                    )

                    result = (
                        portfolio_ai.execute_sell(
                            cash,
                            holdings,
                            code,
                            current_price
                        )
                    )

                    cash = result["cash"]

                    holdings = result["holdings"]

                    if result["sold"]:

                        print(
                            f"SELL: {code} ({reason})"
                        )

            except:
                continue

        # =========================
        # BUY LOOP
        # =========================
        for code in scan_codes:

            try:

                df = (
                    data_map[code]
                    .iloc[:day]
                    .copy()
                )

                if len(df) < 75:
                    continue

                # =========================
                # AI ANALYSIS
                # =========================
                market = market_ai.run(df)

                tech = tech_ai.run(df)

                # 高速化
                news = 0

                inst = inst_ai.run(df)

                # 高速化
                future = 0

                # =========================
                # NORMALIZE
                # =========================
                def normalize_score(x):

                    if x is None:
                        return 0.0

                    if isinstance(x, dict):

                        if "score" in x:
                            return float(x["score"])

                        return 0.0

                    try:
                        return float(x)

                    except:
                        return 0.0

                market = normalize_score(market)

                tech = normalize_score(tech)

                news = normalize_score(news)

                inst = normalize_score(inst)

                future = normalize_score(future)

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
                    "SIG",
                    signal["signal"],
                    signal["confidence"],
                    threshold
                )    
                # =========================
                # PRINT削減
                # =========================
                # print(
                #     f"SCORE={round(signal['confidence'],1)} "
                #     f"{signal['signal']}"
                # )

                # =========================
                # BUY ONLY
                # =========================
                if signal["signal"] != "BUY":

                    continue

                signal_count += 1

                # =========================
                # PRICE
                # =========================
                price = float(
                    df["Close"].iloc[-1]
                )

                # =========================
                # BUY
                # =========================
                result = portfolio_ai.buy(
                    cash,
                    holdings,
                    code,
                    price,
                    signal["confidence"],
                    regime,
                    signal["confidence"]
                )

                cash = result["cash"]

                holdings = result["holdings"]

                if result["bought"]:

                    buy_count += 1

                    print(
                        f"BUY: {code} "
                        f"PRICE={round(price,1)}"
                    )

            except Exception as e:

                print(
                    f"\nERROR CODE: {code}"
                )

                traceback.print_exc()

                continue

        # =========================
        # TOTAL
        # =========================
        total = cash

        for code, pos in holdings.items():

            try:

                current_price = float(
                    data_map[code]["Close"]
                    .iloc[day]
                )

                total += (
                    pos["shares"] *
                    current_price
                )

            except:

                continue
        # DD更新
        dd = portfolio_ai.update_dd(total)
        portfolio_ai.capital.update_dd(dd)
        print(
            f"""
DAY {day} |
SIGNAL {signal_count} |
BUY {buy_count} |
HOLD {hold_count} |
TOTAL {int(total)}
"""
        )

    # =========================
    # FINAL
    # =========================
    final_total = cash

    for code, pos in holdings.items():

        try:

            final_price = float(
                data_map[code]["Close"]
                .iloc[-1]
            )

            final_total += (
                pos["shares"] *
                final_price
            )

        except:

            continue

    print("\n=== FINAL RESULT ===")

    print(
        "FINAL:",
        int(final_total)
    )

    print(
        "POSITIONS:",
        len(holdings)
    )


if __name__ == "__main__":

    run()