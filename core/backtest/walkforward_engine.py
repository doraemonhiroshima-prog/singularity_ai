# core/backtest/walkforward_engine.py

# =====================================================
# IMPORT
# =====================================================

import os
import random
import traceback
import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import evolution

from ai.market_scan_ai import MarketScanAI
from ai.technical_ai import TechnicalAI
from ai.news_ai import NewsAI
from ai.institution_ai import InstitutionAI
from ai.future_prediction_ai import FuturePredictionAI
from ai.strategy_ai import StrategyAI
from ai.signal_ai import SignalAI
from ai.portfolio_ai import PortfolioAI
from ai.investment_ai import InvestmentAI

# =====================================================
# GROWTH
# =====================================================

from core.growth.adaptive_learning import (
    AdaptiveLearning
)

from core.growth.performance_memory import (
    PerformanceMemory
)

from core.growth.monitor import (
    Monitor
)

# =====================================================
# STRATEGY
# =====================================================

from core.strategy.auto_tuner import (
    AutoTuner
)

from core.strategy.winrate_learning import (
    WinRateLearning
)

# =====================================================
# PORTFOLIO
# =====================================================

from core.portfolio.exit_manager import (
    ExitManager
)

# =====================================================
# WALK FORWARD ENGINE V2
# =====================================================

class WalkForwardEngine:

    def __init__(self):

        print(
            "\nRUNNING WALK FORWARD ENGINE V2\n"
        )

        # =================================================
        # DEBUG
        # =================================================

        self.debug = False
        # =================================================
        # TEST MODE
        # =================================================

        self.test_mode = True

        self.test_codes = [

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

        # 営業日ベース（約252日/年）
        self.test_years = 10
        self.test_days = self.test_years * 252
        # =================================================
        # AI FLAGS
        # =================================================

        self.use_news_ai = True

        self.use_future_ai = True

        self.use_institution_learning = True

        self.use_growth_learning = True

        # =================================================
        # CAPITAL
        # =================================================

        self.initial_cash = 3_000_000

        # =================================================
        # DATA SETTINGS
        # =================================================

        self.min_history = 250

        self.test_years = 10

        self.start_day = 240
        
        

        # =================================================
        # FULL MARKET MODE
        # =================================================

        self.max_scan = None

        # =================================================
        # AI
        # =================================================

        self.market_ai = MarketScanAI()

        self.technical_ai = TechnicalAI()

        self.news_ai = NewsAI()

        self.inst_ai = InstitutionAI(
            mode="backtest",
            use_learning=True,
            save_weights=True
        )

        self.future_ai = (
            FuturePredictionAI()
        )

        self.strategy_ai = (
            StrategyAI()
        )

        self.signal_ai = (
            SignalAI()
        )

        # =================================================
        # PORTFOLIO
        # =================================================

        self.portfolio_ai = (
            PortfolioAI(
                self.initial_cash
            )
        )

        self.investment_ai = (
            InvestmentAI(
                self.portfolio_ai
            )
        )
        self.exit_manager = (
            ExitManager()
        )
        
        # =================================================
        # GROWTH
        # =================================================

        self.adaptive_learning = (
            AdaptiveLearning()
        )

        self.performance_memory = (
            PerformanceMemory()
        )

        self.monitor = (
            Monitor()
        )

        self.winrate_learning = (
            WinRateLearning()
        )

        self.auto_tuner = (
            AutoTuner()
        )

        # =================================================
        # LEARNING DATA
        # =================================================

        self.learning_results = []

        # =================================================
        # LOAD
        # =================================================

        self.data_map = (
            self.load_data()
        )

        print(
            f"DATA LOADED : "
            f"{len(self.data_map)} SYMBOLS"
        )
       
# =====================================================
# LOAD DATA
# =====================================================

    def load_data(self):

        data_map = {}

        roots = [
            "data",
            "database",
            "csv",
            "stock_data"
        ]

        csv_files = []

        for root in roots:

            if not os.path.exists(root):
                continue

            for path, dirs, files in os.walk(root):
    
                for file in files:
 
                    if file.endswith(".csv"):
 
                        csv_files.append(
                            os.path.join(path, file)
                        )

        for csv_file in csv_files:
 
            try:
 
                df = pd.read_csv(csv_file)
 
                date_col = None
 
                for col in df.columns:
 
                    if col.lower() in [
                        "date",
                        "datetime",
                        "day"
                    ]:
 
                        date_col = col
                        break
 
                if date_col is None:
                    continue
   
                df["Date"] = pd.to_datetime(
                    df[date_col],
                    errors="coerce"
                )
 
                df = df.dropna(
                    subset=["Date"]
                )
 
                if len(df) < self.min_history:
                    continue
 
                code = os.path.basename(
                    csv_file
                ).replace(
                    ".csv",
                    ""
                )
 
                data_map[code] = df 

            except Exception as e:
  
                if self.debug:
 
                    print(
                        csv_file,
                        e
                    )
 
                continue
 
        print(
            f"LOADED {len(data_map)} SYMBOLS"
        )
 
        return data_map

# =====================================================
# RANDOM TEST PERIOD
# =====================================================

    def random_period(self, df):

         
        size = len(df)

        if size < 500:
         return None

        start = random.randint(
            250,
            size - 250
        )

        end = min(
            size,
            start + 250
        )

        return start, end


# =====================================================
# DATA SLICE
# =====================================================

    def slice_data(
        self,
        df,
        current_index
    ):

        if current_index < self.start_day:

            return None

        return df.iloc[
            : current_index 
        ].copy()


# =====================================================
# FEATURE GENERATION
# =====================================================

    def build_features(self, df):

        close = df["Close"]

        df["MA25"] = (
            close.rolling(25).mean()
        )

        df["MA75"] = (
            close.rolling(75).mean()
        )

        df["HIGH50"] = (
            close.rolling(50).max()
        )

        df["LOW50"] = (
            close.rolling(50).min()
        )

        df["VOL5"] = (
            close.pct_change(fill_method=None)
            .rolling(5)
            .std()
        )

        df["VOL20"] = (
            close.pct_change(fill_method=None)
            .rolling(20)
            .std()
        )

        df["VOL60"] = (
            close.pct_change(fill_method=None)
            .rolling(60)
            .std()
        )

        return df


# =====================================================
# AI ANALYSIS
# =====================================================
    def analyze_ai(
        self,
        code,
        df
    ):

        scores = {
            "market": 0.0,
            "tech": 0.0,
            "news": 0.0,
            "inst": 0.0,
            "future": 0.0
        }

        try:

            scores["market"] = (
                self.market_ai.run(df)
            )

        except:
            pass

        try:

            scores["tech"] = (
                self.technical_ai.run(df)
            )

        except:
            pass

        if self.use_news_ai:

            try:

                scores["news"] = (
                    self.news_ai.run(code)
                )

            except:
                pass

        if self.use_institution_learning:

            try:

                inst_result = (
                    self.inst_ai.run(
                        code,
                        df
                    )
                )

                if isinstance(
                    inst_result,
                    dict
                ):

                    scores["inst"] = (
                        inst_result.get(
                            "score",
                            0
                        )
                    )

                else:

                    scores["inst"] = (
                        inst_result
                    )

            except:
                pass

        if self.use_future_ai:

            try:

                scores["future"] = (
                    self.future_ai.run(df)
                )

            except:
                pass

        return scores
  

# =====================================================
# BUILD SIGNAL
# =====================================================

    def build_signal(
        self,
        scores,
        df
    ):

        strategy = (
            self.strategy_ai.build(
                df
            )        
        )


        #print(
        #    "WEIGHTS:",
        #    strategy["weights"]
        #)

        #print(
        #    "THRESHOLD:",
        ##)

        signal = (
            self.signal_ai.run(

                {
                    "market": scores["market"],
                    "tech": scores["tech"],
                    "news": scores["news"],
                    "inst": scores["inst"],
                    "future": scores["future"]
                },

                strategy["weights"],

                strategy["threshold"]
            )
        )

        #print(
        #    "RAW SIGNAL:",
        #     signal
        #)

        return signal, strategy
# =====================================================
# EVALUATE CODE
# =====================================================

    def evaluate_code(
        self,
        code,
        df
    ):

        try:

            scores = self.analyze_ai(
                code,
                df
            )

            #print(
            #    "SCORES:",
            #    code,
            #    scores
            #)

            #print(
            #    "BEFORE BUILD SIGNAL:",
            #    code
            #)

            signal, strategy = (
                self.build_signal(
                    scores,
                    df
                )
            )

            #print(
            #    "AFTER BUILD SIGNAL:",
            #    code
            #)

            #print(
            #    "SIGNAL RESULT:",
            #    code,
            #    signal
            #)

            #print(
            #    "SIGNAL TYPE:",
            #    signal["signal"]
            #)

            #print(
            #    "CHECKING SIGNAL:",
            #    signal["signal"]
            #)

            if signal["signal"] != "BUY":

                print(
                    "NO SIGNAL:",
                    code
                )

                return None

            #print(
            #    "BUY SIGNAL:",
#                code
#            )

            close = df["Close"]

            price = float(
                close.iloc[-1]
            )

            confidence = float(
                signal.get(
                    "confidence",
                    0
                )
            )


            # =============================================
            # MOMENTUM
            # =============================================

            momentum = (

                close.iloc[-1]

                -

                close.iloc[-20]

            ) / close.iloc[-20]

            bonus = 0

            if momentum > 0.20:

                bonus += 20

            elif momentum > 0.10:

                bonus += 10

            # =============================================
            # BREAKOUT
            # =============================================

            try:

                high50 = (
                    df["HIGH50"]
                    .iloc[-2]
                )

                if close.iloc[-1] > high50:

                    bonus += 15

            except:
                pass

            memory_bonus = 0

            try:

                stat = (
                    self.performance_memory
                    .regime_stats(
                        strategy["regime"]
                    )
                )

                memory_bonus += int(
                    stat.get(
                        "avg_profit",
                        0
                    ) * 10
                )

            except:
                pass

            final_score = (
                confidence
                + bonus
                + memory_bonus
            )

            return {

                "code": code,
                "score": final_score,
                "price": price,
                "confidence": confidence,
                "signal": signal,
                "regime": strategy["regime"],
                "factors": scores
            }
        except Exception as e:

            print(
                "EVALUATE ERROR:",
                code,
                e
            )

            traceback.print_exc()

            return None
# =====================================================
# DAILY LOOP
# =====================================================

    def process_day(
        self,
        day,
        cash,
        holdings,
        trade_logs,
        equity_curve,
        dd_curve,
        peak
    ):

        print(
            "PROCESS_DAY",
            day
        )

        # =============================================
        # BUILD DAY DATA
        # =============================================

        day_data = {}

        for code, df in self.filtered_map.items():

            try:

                if day >= len(df):
                    continue

                sliced = self.slice_data(
                    df,
                    day
                )

                if sliced is None:
                    continue

                day_data[code] = sliced

            except:
                continue

        print(
            "DAY_DATA:",
            len(day_data)
        )

        print(
            "AFTER DAY_DATA"
        )
        print("DAY:", day)

        for code, df in day_data.items():

            print(
                code,
                "LAST CLOSE:",
                float(df["Close"].iloc[-1]),
                "ROWS:",
                len(df)
            )

        cash, holdings, trade_logs = (
            self.process_sell_side(
                day_data,
                cash,
                holdings,
                trade_logs
            )
        )

        print("END SELL")

        candidates = self.build_candidates(
            day_data
        )

        # =============================================
        # BUY
        # =============================================

        cash, holdings, trade_logs = (
            self.process_buy_side(
                candidates,
                cash,
                holdings,
                trade_logs
            )
        )

        print(
            "AFTER BUY SIDE"
        )
        print(final_total)
        print(cash)
        print(holdings)
        # =============================================
        # TOTAL VALUE
        # =============================================

        total = cash

        #print(
        #    "SELL HOLDINGS:",
        #    list(holdings.keys())
        #)

        #print(
        #    "DAY DATA:",
        #    list(day_data.keys())
        #)

        for code, pos in holdings.items():

            try:

                if code not in day_data:

                    print(
                        "NO DAY DATA:",
                        code
                    )

                    continue

                current_price = float(
                    day_data[code]["Close"].iloc[-1]
                )

                shares = pos.get(
                    "shares",
                    0
                )

                total += (
                    shares * current_price
                )

            except:
                continue

        print(
            "TOTAL VALUE:",
            total
        )
        dd = self.portfolio_ai.update_dd(total)
        self.portfolio_ai.capital.update_dd(dd)
        
        equity_curve.append(total)

        peak = max(
            peak,
            total
        )

        dd = (
            peak - total
        ) / peak

        dd_curve.append(dd)

        return (
            cash,
            holdings,
            trade_logs,
            equity_curve,
            dd_curve,
            peak
        )

# =====================================================
# SELL LOGIC
# =====================================================
    def process_sell_side(
        self,
        day_data,
        cash,
        holdings,
        trade_logs
    ):

    #    print("START SELL")

        remove_codes = []

        for code, pos in list(
            holdings.items()
        ):

            try:

            #    print(
            #        "CHECKING EXIT:",
            #        code
            #    )

            #    print(
            #        "ENTRY:",
            #        pos
            #    )

                if code not in day_data:

            #        print(
            #            "NO DAY DATA:",
            #            code
            #        )

                    continue

                df = day_data[code]

                current_price = float(
                    df["Close"].iloc[-1]
                )

            #    print(
            #        "BEFORE SHOULD EXIT",
            #        code
            #    )

                should_exit, reason = (

                    self.portfolio_ai.sell_check(

                        holdings,

                        code,

                        df
                    )
                )

            #    print(
            #        "AFTER SHOULD EXIT",
            #        code,
            #        should_exit,
            #        reason
            #    )

                if not should_exit:
                    continue

                result = (
 
                    self.portfolio_ai
                    .execute_sell(

                        cash,
  
                        holdings,
 
                        code,

                        current_price
                    )
                )

                cash = result["cash"]

                holdings = result["holdings"]
 
                profit = (
 
                     current_price
                    -
                    pos["entry"]
 
                ) / pos["entry"]
 
            #    print(
            #        "SELL:",
            #        code,
            #        "ENTRY:",
            #        pos["entry"],
            #        "EXIT:",
            #        current_price,
            #        "PROFIT:",
            #        profit
            #    )

                self.winrate_learning.update(
                    profit
                )
 
            #    print(
            #        "WINRATE UPDATE:",
            #        profit
            #    )
 
                trade_logs.append({
   
                    "type": "SELL",
  
                    "code": code,
 
                    "price": current_price,
 
                    "profit": profit,
 
                    "reason": reason
                })
 
            #    print(
            #        "SELL:",
            #        code,
            #        "PROFIT:",
            #        round(
            #            profit * 100,
            #            2
            #        ),
            #        "%"
            #    )

                remove_codes.append(
                    code
                )

            except Exception as e:
 
            #    print(
            #        "SELL ERROR:",
            #        code,
            #        e
            #    )
                traceback.print_exc()
                continue
 
        return (
            cash,
            holdings,
            trade_logs
        )

# =============================================
# BUY CANDIDATES
# =====================================================

    def process_buy_side(
        self,
        candidates,
        cash,
        holdings,
        trade_logs
    ):

        for c in candidates:

            try:

                code = c["code"]

                if code in holdings:
                    continue
            #    print(
            #        "TRY BUY:",
            #        code,
            #        c["price"]
            #    )

                result = (

                    self.portfolio_ai.buy(

                        cash,

                        holdings,

                        code,

                        c["price"],

                        c["confidence"],

                        c["regime"],

                        c["confidence"]
                    )
                )
                
                cash = result["cash"] 
                holdings = result["holdings"]

            #    print(
            #        "BUY RESULT:",
            #        result
            #    )
            #    print(
            #        "CASH AFTER BUY:",
            #        cash
            #    )
            #    print(
            #        "HOLDINGS AFTER BUY:",
            #        len(holdings)
            #    )
                
               
            except Exception as e:

            #    print(
            #        "BUY ERROR:",
            #        code,
            #        e
            #    )

                traceback.print_exc()

                continue


        return (
            cash,
            holdings,
            trade_logs
        )
# =====================================================
# BUY CANDIDATES
# =====================================================

    def build_candidates(
        self,
        day_data
    ):

    #    print(
    #        "START BUILD_CANDIDATES"
    #    )

        candidates = []

        for code, df in day_data.items():

            try:

                result = self.evaluate_code(
                    code,
                    df
                )

                if result is None:

                    print(
                       "NO SIGNAL:",
                       code
                    )

                    continue

                print(
                    "ADD CANDIDATE:",
                    code
                )

                candidates.append(result)

                

            except Exception as e:

                print(
                    "EVALUATE ERROR:",
                    code,
                    e
                )

                traceback.print_exc()

                continue

        print(
            "BUILD FINISHED:",
            len(candidates)
        )

    # 上位10件だけ表示
        for c in candidates[:10]:

            try:

                print(
                    "SIG",
                    c["code"],
                    round(
                        c["score"],
                        2
                    )
                )

            except:
                pass

        candidates.sort(

            key=lambda x:
            x["confidence"],

            reverse=True
        )
        return candidates
# =====================================================
# PERFORMANCE LEARNING
# =====================================================

    def update_learning(
        self,
        trade_logs
    ):

        try:

            sells = [

                t

                for t in trade_logs

                if t["type"]
                == "SELL"
            ]

            if not sells:
                return

            profits = [

                x["profit"]

                for x in sells
            ]

            avg_profit = (
                np.mean(profits)
            )

            winrate = (

                len(

                    [

                        x

                    for x in profits

                    if x > 0
                    ]

                )

                /

                len(profits)
            )

            self.learning_results.append({

                "profit":
                    avg_profit,

                "winrate":
                    winrate,

                "trades":
                    len(sells)
            })

        except:

            pass


# =====================================================
# SAVE LEARNING
# =====================================================

    def save_learning_data(
        self
    ):

        try:

            if not (
                self.learning_results
            ):
                return

            self.monitor.save_learning_data(

                self.learning_results
            )

        except:

            pass


# =====================================================
# EQUITY METRICS
# =====================================================

    def calculate_metrics(
        self,
        equity_curve,
        dd_curve,
        trade_logs
    ):

        if len(equity_curve) == 0:

            return {
                "final": self.initial_cash,
                "cagr": 0,
                "max_dd": 0,
                "trades": 0,
                "winrate": 0
            }

        final = equity_curve[-1]

        final = (
            equity_curve[-1]
        )

        years = (
            self.test_years
        )

        cagr = (

            (

                final

                / 

                self.initial_cash

            )

            **

            (
                1 / years
            )

        ) - 1

        max_dd = max(
            dd_curve
        )

        wins = len([

           x

            for x in trade_logs

            if (
                x["type"]
                == "SELL"

                and

                x.get(
                    "profit",
                    0
                ) > 0
            )
        ])

        sells = len([

            x

            for x in trade_logs

            if x["type"]
            == "SELL"
        ])

        if sells > 0:

            winrate = (
                wins / sells
            )

        else:

            winrate = 0

        return {

            "final":
                final,

            "cagr":
                cagr,

            "max_dd":
                max_dd,

            "trades":
                len(trade_logs),

            "winrate":
                winrate
        }
# =====================================================
# RUN
# =====================================================

    def run(self):

        start_year, end_year = (
            self.random_period_years()
        )

        print("\n========================")
        print(
            "WALK FORWARD V2"
        )
        print(
            start_year,
            "~",
            end_year
        )
        print("========================\n")

# =================================================
# FILTER
# =================================================

        filtered_map = {}

        for code, df in (
            self.data_map.items()
        ):

            try:

                filtered = df[

                    (
                        df["Date"]
                        .dt.year
                    >= start_year
                    )

                    &

                    (
                        df["Date"]
                        .dt.year
                        <= end_year
                    )
   
                ].copy()

                filtered = (
                    filtered
                    .reset_index(
                        drop=True
                    )
                )

                if len(filtered) < (
                    self.min_history
                ):
                    continue

                filtered = (
                    self.build_features(
                        filtered
                    )
                )

                filtered_map[
                    code
                ] = filtered

            except:

                continue

        if not filtered_map:

            raise Exception(
                "NO DATA"
            )

        self.filtered_map = (
            filtered_map
        )
        self.start_year = start_year
        self.end_year = end_year

        sample_df = next(iter(filtered_map.values()))

        self.start_date = sample_df["Date"].iloc[0]
        self.end_date = sample_df["Date"].iloc[-1]
# ==========================================
# TEST CODE FILTER
# ==========================================

        if self.test_mode:

            self.filtered_map = {
 
                code: df
  
                for code, df in self.filtered_map.items()
  
                if code in self.test_codes
   
            }
  
            print(
  
                "TEST CODES:",
   
                list(self.filtered_map.keys())
  
            )
# =================================================
# MAX DAYS
# =================================================

        max_days = min(
            len(df)
            for df in self.filtered_map.values()
        )

        print(
            "SYMBOLS :",
            len(filtered_map)
        )

        print(
            "MAX DAYS :",
            max_days
        )
        print("SELF_FILTERED_MAP :", len(self.filtered_map))

        for code, df in self.filtered_map.items():
            print(code, len(df))
# =================================================
# PORTFOLIO
# ===================================
# ==============

        cash = (
            self.initial_cash
        )

        holdings = {}

        trade_logs = []

        equity_curve = []

        dd_curve = []

        peak = cash
         
# =================================================
# MAIN LOOP
# =================================================

        end_day = max_days

        if self.test_mode:

                end_day = min(

                max_days,     

                self.start_day + self.test_days

            )  

        for day in range(

            self.start_day,

            end_day

        ):

            try:

                if day % 10 == 0:

                    print(

                        "DAY",

                        day,

                        "CASH",

                        int(cash),

                        "HOLD",

                        len(
                            holdings
                        )
                    )

                (
                    cash,

                    holdings,
  
                    trade_logs,
 
                    equity_curve,

                    dd_curve,
 
                    peak

                ) = self.process_day(
 
                    day,

                    cash,
 
                    holdings,
 
                    trade_logs,
 
                    equity_curve,
 
                    dd_curve,
 
                    peak
                )

# =========================================
# GROWTH UPDATE
# =========================================

                if (
 
                   self.use_growth_learning
 
                    and
 
                    day % 20 == 0
                ):
 
                    try:
     
                        self.update_learning(
                            trade_logs
                        )

                    except:
 
                        pass
 
            except Exception as e:
 
                if self.debug:
 
                    print(
                     e
                    )
 
                    traceback.print_exc()
 
                continue

# =================================================
# FINAL LEARNING
# =================================================

        try:
 
            self.save_learning_data()
 
        except:
 
            pass

# =================================================
# ADAPTIVE LEARNING SAVE
# =================================================

        try:
 
            self.adaptive_learning.optimize()
 
        except:
 
            pass

# =================================================
# PERFORMANCE MEMORY SAVE
# =================================================

        try:
 
            self.performance_memory.save()
 
        except:
 
            pass

# =================================================
# METRICS
# =================================================

        result = (
            self.calculate_metrics(
 
                equity_curve,
   
                dd_curve,
 
                trade_logs
            )
        )
        self.start_year = start_year
        self.end_year = end_year

        sample_df = next(iter(filtered_map.values()))

        self.start_date = sample_df["Date"].iloc[0]
        self.end_date = sample_df["Date"].iloc[-1]
        return {
 
            "result":
                result,
 
            "equity_curve":
                equity_curve,
 
            "dd_curve":
                dd_curve,
 
            "trades":
                trade_logs
        }
# =====================================================
# RANDOM PERIOD YEARS
# =====================================================

    def random_period_years(self):

        years = []

        for df in self.data_map.values():

            try:

                years.extend(
                    list(
                        df["Date"]
                        .dt.year
                        .unique()
                    )
                )

            except:
                continue

        years = sorted(
            list(
                set(years)
            )
        )

        if len(years) == 0:

            raise Exception(
                "NO VALID YEARS"
            )

        if len(years) < 12:

            return (
                years[0],
                years[-1]
            )

        start_year = 2005
        end_year = 2015

        return (
            start_year,
            end_year
        )
# =====================================================
# GROWTH FEEDBACK
# =====================================================

    def apply_growth_feedback(
        self
    ):
 
        try:
 
            stats = (
 
                self.performance_memory
                .summary()
            )
 
            if not stats:
                return
 
            winrate = stats.get(
                "winrate",
                0.5
            )
 
            avg_profit = stats.get(
                "profit",
                0
            )
 
            if winrate > 0.60:
 
                self.auto_tuner.base_threshold += 2
 
            elif winrate < 0.45:
 
                self.auto_tuner.base_threshold -= 2
 
            if avg_profit > 0.15:
 
                self.auto_tuner.base_threshold += 2
 
            elif avg_profit < 0:
 
                self.auto_tuner.base_threshold -= 2

            self.auto_tuner.base_threshold = max(
 
                5,

                min(
                    40,
                    self.auto_tuner.base_threshold
                )
            )

        except:
 
            pass
# =====================================================
# SAVE CHARTS
# =====================================================

    def save_charts(
        self,
        equity_curve,
        dd_curve
    ):

        try:
 
            plt.figure(
                figsize=(16, 8)
            )

            plt.plot(
                equity_curve
            )

            plt.title(
                "EQUITY CURVE"
            )
 
            plt.grid(True)
 
            plt.savefig(
                "equity_curve.png"
            )

            plt.close()

        except:

            pass

        try:

            plt.figure(
                figsize=(16, 5)
            )

            plt.plot(
                dd_curve
            )

            plt.title(
                "DRAWDOWN"
            )

            plt.grid(True)

            plt.savefig(
                "drawdown_curve.png"
            )

            plt.close()

        except:

            pass
# =====================================================
# SHARPE
# =====================================================

    def calculate_sharpe(
        self,
        equity_curve
    ):

        try:
 
            if len(
                equity_curve
            ) < 30:
 
                return 0
 
            returns = pd.Series(
                equity_curve
            ).pct_change()
 
            returns = (
                returns
                .dropna()
            )
 
            if len(
                returns
            ) == 0:
 
                return 0
 
            std = returns.std()

            if std == 0:
 
                return 0
 
            sharpe = (
 
                returns.mean()

                /
 
                std
 
            ) * math.sqrt(
                252
            )

            return round(
                sharpe,
                2
            )

        except:
 
            return 0
# =====================================================
# PROFIT FACTOR
# =====================================================

    def calculate_pf(
        self,
        trade_logs
    ):
 
        try:
    
            gains = 0

            losses = 0

            for t in trade_logs:
 
                if t.get(
                    "type"
                ) != "SELL":
 
                    continue

                profit = t.get(
                    "profit",
                    0
                )

                if profit > 0:
 
                    gains += profit
 
                else:
 
                    losses += abs(
                        profit
                    )

            if losses == 0:
 
                return round(
                    gains,
                    2
                )
 
            return round(
 
                gains
 
                /
 
                losses,
 
                2
            )

        except:

            return 0
# =====================================================
# FINAL REPORT
# =====================================================

    def build_report(
        self,
        result,
        equity_curve,
        dd_curve,
        trade_logs
    ):

        sharpe = (
            self.calculate_sharpe(
                equity_curve
            )
        )

        pf = (
            self.calculate_pf(
                trade_logs
            )
        )

        self.save_charts(

            equity_curve,

            dd_curve
        )
        print("\n===== BACKTEST PERIOD =====")
        print(
            "YEAR :",
            self.start_year,
            "~",
            self.end_year
        )
        print(
            "START :",
            self.start_date.strftime("%Y-%m-%d")
        )
        print(
            "END :",
            self.end_date.strftime("%Y-%m-%d")
        )

        print(
            "\n===================="
        )
        
        print(
            "FINAL:",
            int(
                result["final"]
            )
        )

        print(
            "CAGR:",
            round(
                result["cagr"] * 100,
                2
            ),
            "%"
        )

        print(
            "MAX DD:",
            round(
                result["max_dd"] * 100,
                2
            ),
            "%"
        )

        print(
            "WINRATE:",
            round(
               result["winrate"]
                * 100,
                2
            ),
            "%"
        )

        print(
            "PF:",
            pf
        )

        print(
            "SHARPE:",
            sharpe
        )

        print(
            "TRADES:",
            result["trades"]
        )

        print(
            "===================="
        )
        

        return {

            "final":
                result["final"],

            "cagr":
                result["cagr"],

            "max_dd":
                result["max_dd"],

            "winrate":
                result["winrate"],

            "pf":
                pf,

            "sharpe":
                sharpe,

            "trades":
                result["trades"]
        }
# =====================================================
# EVOLUTION RETURN
# =====================================================

    def run_for_evolution(
        self  
    ):
        print("===================" \
        "")
        print("RUN EVOLUTION")
        print("===================")
        
        if not hasattr(self, "filtered_map"):
            self.run()

        result = evolution.run(
            data_map=self.filtered_map
        )   
        
        print("===== RESULT =====")

        for k, v in result.items():

            if k == "holdings":
                continue

            print(k, ":", v)

        print("==================")
        print("===================")
        print("WALK FORWARD V2 END")
        print("===================")
        
        return result
        
# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    print("\nSTART WALK FORWARD V2\n")

    engine = WalkForwardEngine()

    engine.run()               # ← これでfiltered_mapが作られる

    engine.run_for_evolution() # ← その後にevolution