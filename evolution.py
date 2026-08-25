   #evolution.py

import random
import traceback
import numpy as np
import time
import os
import pandas as pd
import matplotlib.pyplot as plt

from concurrent.futures import ThreadPoolExecutor
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
from ai.investment_ai import InvestmentAI
import ai.portfolio_ai as p
from ai.growth_ai import GrowthAI

PortfolioAI = p.PortfolioAI

print("USING:", p.__file__)


# =========================================================
# CONTROL PANEL
# =========================================================

USE_MARKET_AI =False

USE_TECH_AI = True

USE_NEWS_AI = False

USE_INSTITUTION_AI = False

USE_FUTURE_AI = False

USE_SIGNAL_AI = True

USE_STRATEGY_AI = False

USE_RANDOM_SCAN = False

USE_INSTITUTION_LEARNING = False


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
# WALKFORWARD
# =========================================================
def analyze_code(

    code,

    name,

    df,

    cash,

    holdings,

    market_ai,

    tech_ai,

    news_ai,

    inst_ai,






    future_ai,

    signal_ai,

    strategy_ai,

    growth_ai,

    growth_weights
):
   
    # =========================================
    # MARKET
    # =========================================
    if USE_MARKET_AI:

        market = normalize_score(
            market_ai.run(df)
        )

    else:

        market = 50
    
    # =========================================
    # TECH
    # =========================================
    if USE_TECH_AI:

        tech = normalize_score(
            tech_ai.run(df)
        )

    else:

        tech = 50
    
    # =========================================
    # NEWS
    # =========================================
    if USE_NEWS_AI:

        news = normalize_score(

            news_ai.run(
                code,
                name,
                df
            )
        )

    else:
 
        news = 50

    # =========================================
    # INSTITUTION
    # =========================================
    if USE_INSTITUTION_AI:

        inst_result = inst_ai.run(df)

        inst = normalize_score(
            inst_result
        )

    else:

        inst_result = {}

        inst = 50

    # =========================================
    # FUTURE
    # =========================================
    if USE_FUTURE_AI:

        future_result = future_ai.run(df)
        future = normalize_score(future_result)

    else:

        future_result = {}
        future = 50

    # =========================================
    # STRATEGY
    # =========================================
    if USE_STRATEGY_AI:

        strategy = strategy_ai.build(df)

        regime = strategy["regime"]
        weights = strategy["weights"]
        threshold = strategy["threshold"]

    else:

        regime = "NORMAL"

        weights = {
            "market": 0.2,
            "tech": 0.2,
            "news": 0.2,
            "inst": 0.2,
            "future": 0.2
        }

        threshold = 60
    # =========================================
    # GROWTH AI WEIGHTS
    # =========================================
    if growth_weights:

        weights = {
            "market": growth_weights.get("market", weights["market"]),
            "tech": growth_weights.get("tech", weights["tech"]),
            "news": growth_weights.get("news", weights["news"]),
            "inst": growth_weights.get("inst", weights["inst"]),
            "future": growth_weights.get("future", weights["future"])
        }    
    
    # =========================================
    # SIGNAL
    # =========================================
    if USE_SIGNAL_AI:
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
    else:

        signal = {
            "signal": "NONE",
            "confidence": 50
        }
    return {

        "signal": signal,

        "regime": regime,

        "inst_detail": inst_result,

        "threshold": threshold

    }

# =========================================================
# MAIN
# =========================================================
def run(data_map=None):

    # =====================================================
    # AI INITIALIZE
    # =====================================================
    data_ai = DataAI()

    market_ai = MarketScanAI()

    tech_ai = TechnicalAI()

    news_ai = NewsAI()

    growth_ai = GrowthAI()

    growth_weights = growth_ai.learning.weights()
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
    investment_ai = InvestmentAI(
    portfolio_ai
)
    # =====================================================
    # TEST CODES
    # =====================================================
    codes = [

        "7203.T",  # トヨタ自動車
        "6758.T",  # ソニーグループ
        "9432.T",  # NTT
        "8306.T",  # 三菱UFJFG
        "6501.T",  # 日立製作所

        "4063.T",  # 信越化学工業
        "8035.T",  # 東京エレクトロン
        "8058.T",  # 三菱商事
        "2914.T",  # 日本たばこ産業（JT）
        "4502.T",  # 武田薬品工業

    ]

    # =====================================================
    # LOAD DATA
    # =====================================================
    if data_map is None:
        result = data_ai.run(codes)

        data_map = result["market_data"]
    
        stock_info = result.get(
        "stock_info",
        {}
        )
    else:

        stock_info = {}
    if len(data_map) == 0:

        print("NO DATA")

        return

    print("DATA:", len(data_map))
    print("DATA RANGE:",
          min(df["Date"].min() for df in data_map.values()),
          "~",
          max(df["Date"].max() for df in data_map.values()))
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
    results = []
    peak = cash
    max_dd = 0
    
    # ==========================================
    # EQUITY LOG
    # ==========================================
    equity_log = []
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
        codes = list(data_map.keys())
            
        if USE_RANDOM_SCAN:
            random.shuffle(codes)
            codes = codes[:500]
        else:
            codes = sorted(codes)

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

                        results.append({
                            "code": code,

                            "entry_day": pos.get(
                                "entry_day",
                                0
                            ),

                            "exit_day": day,

                            "profit": (
                                current_price - pos["entry"]
                            ) / pos["entry"],

                            "entry": pos["entry"],

                            "exit": current_price,

                            "factors": pos.get(
                                "inst_detail",
                                {}
                            ),

                            "regime": pos.get(
                                "regime",
                                "UNKNOWN"
                            )
                        })    

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
                # PRICE
                # =========================================
                price = float(

                    df["Close"]
                    .iloc[-1]

                )
                # =========================================
                # NAME
                # =========================================
                name = stock_info.get(
                    code,
                    code
                )

                # =========================================
                # AI ANALYZE
                # =========================================
                import time

                t0 = time.perf_counter()
                
                result = analyze_code(

                    code,

                    name,

                    df,

                    cash,

                    holdings,

                    market_ai,

                    tech_ai,

                    news_ai,

                    inst_ai,

                    future_ai,

                    signal_ai,

                    strategy_ai,

                    growth_ai,
                    
                    growth_weights
                )

                signal = result["signal"]

                regime = result["regime"]

                inst_result = result["inst_detail"]
                
            #    print("ANALYZE:", round(time.perf_counter() - t0, 3), "秒")

                # =========================================
                # BUY ONLY
                # =========================================
                if signal["signal"] != "BUY":

                    continue
                if not investment_ai.decide(
                    signal,
                    holdings,
                    cash,
                    portfolio_ai.current_dd

                ):

                    continue
                signal_count += 1

                # PRICE
                price = float(
                    df["Close"].iloc[-1]
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

                    holdings[code][
                        "entry_day"
                    ] = day

                    holdings[code][
                        "regime"
                    ] = regime
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
        print(
            "HOLDINGS:",
            {
                code: pos["shares"]
                for code, pos in holdings.items()
            }
        )
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
    # =========================================
    # EQUITY LOG
    # =========================================
        
        equity_log.append({

            "Day": day,

            "Total": total,
 
            "Cash": cash,
 
            "Positions": len(holdings),
 
            "DrawDown": max_dd
 
        })

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
HOLD {len(holdings)} |
TOTAL {int(total)}
"""
        )


    for code, pos in holdings.items():

        try:

            final_price = float(
                data_map[code]["Close"].iloc[-1]
            )
            
        except:

            continue
    # =====================================================
    # GROWTH AI
    # =====================================================
    if results:

        growth_result = growth_ai.run(
            results
        )
        growth_weights = growth_result["weights"]
        print(
            "GROWTH AI:",
            growth_result
        )
         # 実際のポートフォリオDD
        growth_result["metrics"]["dd"] = max_dd
        print(
            "GROWTH METRICS:",
            growth_result["metrics"]
        )

        print(
            "GROWTH WEIGHTS:",
            growth_result["weights"]
        )

        print(
            "GROWTH WINRATE:",
            growth_result["memory_winrate"]
        )

        print(
            "GROWTH AVG PROFIT:",
            growth_result["memory_profit"]
        )
    # =====================================================
    # FINAL
    # =====================================================
    final_total = cash

    print("FINAL CASH CHECK:", cash)

    for code, pos in holdings.items():

        try:

            final_price = float(
                  data_map[code]["Close"].iloc[day]
            )

            value = pos["shares"] * final_price

            print(
                "FINAL CHECK:",
                code,
                "SHARES:",
                pos["shares"],
                "PRICE:",
                final_price,
                "VALUE:",
                value
            )

            final_total += value

        except:

            continue
    # =====================================================
    # SAVE GRAPH
    # =====================================================
    import os
    import pandas as pd
    import matplotlib.pyplot as plt

    os.makedirs("logs", exist_ok=True)

    # CSV保存
    df = pd.DataFrame({
        "Day":[x["Day"] for x in equity_log],
        "Asset":[x["Total"] for x in equity_log]
 
    })
 
    csv_path = "logs/equity_curve.csv"
 
    df.to_csv(
 
        csv_path,
 
        index=False,
 
        encoding="utf-8-sig"
 
    )
 
    # =========================
    # GRAPH
    # =========================
    plt.figure(figsize=(12,6))
 
    plt.plot(
        [x["Total"] for x in equity_log],
        linewidth=2
    )
 
    

    plt.title("Ω SINGULARITY AI Equity Curve") 
 
    plt.xlabel("Day")
 
    plt.ylabel("Total Assets (JPY)")


    # =========================
    # 金額表示
    # =========================
    import matplotlib.ticker as ticker

    plt.gca().yaxis.set_major_formatter(
        ticker.FuncFormatter(
            lambda x, pos: f"{int(x):,}"
        )
    )


    plt.grid(True)
  
    png_path = "logs/equity_curve.png"
  
    plt.savefig(
  
        png_path,
 
        dpi=150,
 
        bbox_inches="tight"
 
    )
 
    plt.close()
 
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

# =====================================================
# RETURN RESULT
# =====================================================

    return {

        "final": final_total,

        "max_dd": max_dd,
 
        "positions": len(holdings),
 
        "cash": cash, 
  
        "holdings": holdings
 
    }
# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":

    run()