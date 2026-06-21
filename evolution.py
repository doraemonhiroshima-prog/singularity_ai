  #evolution.py

import random
import traceback
import numpy as np

from ai.data_ai import DataAI
from ai.market_scan_ai import MarketScanAI
from ai.technical_ai import TechnicalAI
from ai.news_ai import NewsAI
from ai.future_prediction_ai import (
    FuturePredictionAI
)
from ai.institution_ai import InstitutionAI
from ai.signal_ai import SignalAI
from ai.strategy_ai import StrategyAI

import ai.portfolio_ai as p

PortfolioAI = p.PortfolioAI

print("USING:", p.__file__)


# =========================================================
# CONTROL PANEL
# =========================================================

USE_NEWS_AI = True

USE_FUTURE_AI = True

USE_RANDOM_SCAN = True

USE_INSTITUTION_LEARNING = True

SCAN_LIMIT = 10

START_DAY = 240

MAX_TEST_DAYS = 365


# =========================================================
# NORMALIZE
# =========================================================
def normalize_score(result):

    if result is None:

        return 0.0

    # =====================================================
    # DICT
    # =====================================================
    if isinstance(result, dict):

        score = result.get(
            "score",
            0
        )

    else:

        score = result

    # =====================================================
    # FLOAT
    # =====================================================
    try:

        score = float(score)

    except:

        score = 0.0

    # =====================================================
    # LIMIT
    # =====================================================
    score = max(
        min(score, 100),
        0
    )

    return score


# =========================================================
# MAIN
# =========================================================
def run():

    # =====================================================
    # AI INITIALIZE
    # =====================================================
    data_ai = DataAI()

    market_ai = MarketScanAI()

    tech_ai = TechnicalAI()

    news_ai = NewsAI()

    # =====================================================
    # INSTITUTION
    # =====================================================
    inst_ai = InstitutionAI(

        mode="live",

        use_learning=
            USE_INSTITUTION_LEARNING,

        save_weights=False
    )

    future_ai = FuturePredictionAI()

    signal_ai = SignalAI()

    strategy_ai = StrategyAI()

    portfolio_ai = PortfolioAI(
        3000000
    )

    # =====================================================
    # TEST CODES
    # =====================================================
    codes = [

        "7203.T",
        "6758.T",
        "9984.T",
        "9432.T",
        "8306.T",

        "6861.T",
        "7011.T",
        "6501.T",
        "4063.T",
        "6098.T"
    ]

    # =====================================================
    # LOAD DATA
    # =====================================================
    result = data_ai.run(codes)

    data_map = result["market_data"]
    
    stock_info = result.get(
    "stock_info",
    {}
    )

    if len(data_map) == 0:

        print("NO DATA")

        return

    print("DATA:", len(data_map))

    # =====================================================
    # MAX DAYS
    # =====================================================
    max_days = min([

        len(df)

        for df in data_map.values()

    ])

    max_days = min(
        max_days,
        MAX_TEST_DAYS
    )

    print("MAX DAYS:", max_days)

    # =====================================================
    # PORTFOLIO
    # =====================================================
    cash = 3000000

    holdings = {}

    peak = cash
    max_dd = 0

    # =====================================================
    # MAIN LOOP
    # =====================================================
    for day in range(

        START_DAY,

        max_days

    ):

        signal_count = 0

        buy_count = 0

        hold_count = len(holdings)

        # =================================================
        # RANDOM SCAN
        # =================================================
        codes = list(
            data_map.keys()
        )

        random.shuffle(codes)

        codes = codes[:500]

        # =================================================
        # FINAL SCAN
        # =================================================
        if USE_RANDOM_SCAN:

            scan_codes = codes[
                :SCAN_LIMIT
            ]

        else:

            scan_codes = codes

        # =================================================
        # SELL CHECK
        # =================================================
        for code, pos in list(
            holdings.items()
        ):

            try:

                df = (

                    data_map[code]
                    .iloc[:day]
                    .copy()

                )

                # =========================================
                # SELL CHECK
                # =========================================
                should_sell, reason = (

                    portfolio_ai.sell_check(

                        holdings,

                        code,

                        df
                    )
                )

                # =========================================
                # SELL
                # =========================================
                if should_sell:

                    current_price = float(

                        df["Close"]
                        .iloc[-1]

                    )

                    result = (

                        portfolio_ai
                        .execute_sell(

                            cash,

                            holdings,

                            code,

                            current_price
                        )
                    )

                    cash = result["cash"]

                    holdings = result["holdings"]

                    # =====================================
                    # LEARNING
                    # =====================================
                    if USE_INSTITUTION_LEARNING:

                        try:

                            inst_detail = pos.get(
                                "inst_detail",
                                {}
                            )

                            pnl = (

                                current_price -

                                pos["entry"]

                            ) / pos["entry"]

                            inst_ai.core.learn(

                                flow_score=
                                    inst_detail.get(
                                        "flow_score",
                                        50
                                    ),

                                pressure_score=
                                    inst_detail.get(
                                        "pressure_score",
                                        50
                                    ),

                                order_score=
                                    inst_detail.get(
                                        "order_score",
                                        50
                                    ),

                                profit_pct=pnl
                            )

                        except Exception as e:

                            print(
                                "LIVE LEARN ERROR:",
                                e
                            )

                    # =====================================
                    # LOG
                    # =====================================
                    if result["sold"]:

                        print(

                            f"SELL: {code} "

                            f"({reason})"
                        )

            except Exception:

                continue

        # =================================================
        # BUY LOOP
        # =================================================
        for code in scan_codes:

            try:

                df = (

                    data_map[code]
                    .iloc[:day]
                    .copy()

                )

                if len(df) < 75:

                    continue

                # =========================================
                # MARKET
                # =========================================
                market = normalize_score(

                    market_ai.run(df)

                )

                # =========================================
                # TECH
                # =========================================
                tech = normalize_score(

                    tech_ai.run(df)

                )

                # =========================================
                # NEWS
                # =========================================
                if USE_NEWS_AI:

                    name = stock_info.get(
                        code,
                        code
                    )

                    news_result = news_ai.run(
                        code,
                        name,
                        df
                    )

                    news = normalize_score(
                        news_result
                    )
                   

                else:

                    news = 0.0

                # =========================================
                # INSTITUTION
                # =========================================
                inst_result = (
                    inst_ai.run(df)
                )

                inst = normalize_score(
                    inst_result
                )

                # =========================================
                # FUTURE
                # =========================================
                if USE_FUTURE_AI:

                    future = normalize_score(

                        future_ai.run(df)

                    )

                else:

                    future = 0.0

                # =========================================
                # STRATEGY
                # =========================================
                strategy = (
                    strategy_ai.build(df)
                )

                regime = strategy["regime"]

                weights = strategy["weights"]

                threshold = strategy["threshold"]

                # =========================================
                # SIGNAL
                # =========================================
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

                    round(
                        signal["confidence"],
                        2
                    ),

                    threshold
                )

                # =========================================
                # BUY ONLY
                # =========================================
                if signal["signal"] != "BUY":

                    continue

                signal_count += 1

                # =========================================
                # PRICE
                # =========================================
                price = float(

                    df["Close"]
                    .iloc[-1]

                )

                # =========================================
                # BUY
                # =========================================
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

                # =========================================
                # SAVE DETAIL
                # =========================================
                if code in holdings:

                    holdings[code][
                        "inst_detail"
                    ] = inst_result

                    holdings[code][
                        "entry"
                    ] = price

                # =========================================
                # LOG
                # =========================================
                if result["bought"]:

                    buy_count += 1

                    print(

                        f"BUY: {code} "

                        f"PRICE={round(price,1)}"
                    )

            except Exception:

                print(
                    f"\nERROR CODE: {code}"
                )

                traceback.print_exc()

                continue

        # =================================================
        # TOTAL
        # =================================================
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
        peak = max(
             peak,
             total
        )

        dd = ( 
            peak - total
        ) / peak

        max_dd = max(
            max_dd,
            dd
        )
        # =================================================
        # DD
        # =================================================
        dd = portfolio_ai.update_dd(
            total
        )

        portfolio_ai.capital.update_dd(
            dd
        )

        # =================================================
        # LOG
        # =================================================
        print(

            f"""
DAY {day} |
SIGNAL {signal_count} |
BUY {buy_count} |
HOLD {hold_count} |
TOTAL {int(total)}
"""
        )

    # =====================================================
    # FINAL
    # =====================================================
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

    # =====================================================
    # RESULT
    # =====================================================
    print("\n=== FINAL RESULT ===")

    print(
        "FINAL:",
        int(final_total)
    )
    print(
    "MAX DD:",
    round(max_dd * 100, 2),
    "%"
    )
    print(
        "POSITIONS:",
        len(holdings)
    )


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":

    run()