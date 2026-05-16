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

        # 軽量化
        codes = list(data_map.keys())

        random.shuffle(codes)

        # ★ まずは10銘柄だけ
        scan_codes = codes[:10]

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

                news = 0


                inst = inst_ai.run(df)

                future = future_ai.run(df)

                # =========================
                # 数値統一
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

                        return float(x)

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
                # SCORE MONITOR
                # =========================
                

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
                    f"SCORE={round(signal['confidence'],1)} "
                    f"{signal['signal']}"
                )

                # =========================
                # BUY SIGNAL
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
                    regime
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

                 import traceback

                 print(f"\nERROR CODE: {code}")

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
