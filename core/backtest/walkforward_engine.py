# core/backtest/walkforward_engine.py

import os
import random
import pandas as pd
import matplotlib.pyplot as plt

from ai.market_scan_ai import MarketScanAI
from ai.technical_ai import TechnicalAI
from ai.news_ai import NewsAI
from ai.institution_ai import InstitutionAI

from core.growth.adaptive_learning import AdaptiveLearning
from core.portfolio.exit_manager import ExitManager


class WalkForwardEngine:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(self):

        print("RUNNING WALK FORWARD ENGINE")

        # =========================
        # DEBUG
        # =========================
        self.debug = False

        # =========================
        # AI
        # =========================
        self.market_ai = MarketScanAI()

        self.technical_ai = TechnicalAI()

        self.news_ai = NewsAI()

        self.inst_ai = InstitutionAI()

        self.learning = AdaptiveLearning()

        self.exit_manager = ExitManager()

        # =========================
        # SETTINGS
        # =========================
        self.initial_cash = 3_000_000

        self.max_positions = 5

        self.min_history = 120

        self.top_n = 5

        self.entry_threshold = 35

        # =========================
        # LOAD DATA
        # =========================
        self.data_map = self.load_data()

    # =====================================================
    # LOAD DATA
    # =====================================================
    def load_data(self):

        data_map = {}

        folder = "data"

        files = [
            f for f in os.listdir(folder)
            if f.endswith(".csv")
        ]

        print("\nLOADING DATA...")

        for file in files:

            try:

                path = os.path.join(
                    folder,
                    file
                )

                df = pd.read_csv(path)

                if len(df) < 1500:
                    continue

                if "Date" not in df.columns:
                    continue

                # =========================
                # DATE
                # =========================
                df["Date"] = pd.to_datetime(
                    df["Date"]
                )

                df = df.sort_values(
                    "Date"
                )

                # =========================
                # PRE CALC
                # =========================
                df["MA25"] = (
                    df["Close"]
                    .rolling(25)
                    .mean()
                )

                df["HIGH50"] = (
                    df["Close"]
                    .rolling(50)
                    .max()
                )

                df["VOL20"] = (
                    df["Volume"]
                    .rolling(20)
                    .mean()
                )

                code = file.replace(
                    ".csv",
                    ""
                )

                data_map[code] = (
                    df.reset_index(drop=True)
                )

            except Exception as e:

                if self.debug:

                    print(
                        "LOAD ERROR:",
                        file,
                        e
                    )

        print("DATA:", len(data_map))

        return data_map

    # =====================================================
    # RANDOM PERIOD
    # =====================================================
    def random_period(self):

        start_year = random.randint(
            2005,
            2015
        )

        end_year = start_year + 10

        return (
            start_year,
            end_year
        )

    # =====================================================
    # FAST SLICE
    # =====================================================
    def slice_data(
        self,
        day
    ):

        sliced = {}

        for code, df in self.data_map.items():

            try:

                # =====================
                # DAY CHECK
                # =====================
                if len(df) <= day:
                    continue

                # =====================
                # FAST ILOC
                # =====================
                sub = df.iloc[:day]

                if len(sub) < self.min_history:
                    continue

                sliced[code] = sub

            except:
                continue

        return sliced

    # =====================================================
    # EVALUATE
    # =====================================================
    def evaluate_code(
        self,
        item
    ):

        code, df = item

        try:

            # =========================
            # TECH
            # =========================
            tech_score = 50

            try:

                tech = (
                    self.technical_ai
                    .run(df)
                )

                if isinstance(
                    tech,
                    dict
                ):

                    tech_score = float(
                        tech.get(
                            "score",
                            50
                        )
                    )

                else:

                    tech_score = float(tech)

            except Exception as e:

                if self.debug:

                    print(
                        code,
                        "TECH ERROR:",
                        e
                    )

            # =========================
            # MARKET
            # =========================
            market_score = 50

            try:

                market = (
                    self.market_ai
                    .run(df)
                )

                if isinstance(
                    market,
                    dict
                ):

                    market_score = float(
                        market.get(
                            "score",
                            50
                        )
                    )

                else:

                    market_score = float(market)

            except Exception as e:

                if self.debug:

                    print(
                        code,
                        "MARKET ERROR:",
                        e
                    )

            # =========================
            # INSTITUTION
            # =========================
            inst_score = 50

            try:

                inst = (
                    self.inst_ai
                    .run(df)
                )

                if isinstance(
                    inst,
                    dict
                ):

                    inst_score = float(
                        inst.get(
                            "score",
                            50
                        )
                    )

                else:

                    inst_score = float(inst)

            except Exception as e:

                if self.debug:

                    print(
                        code,
                        "INST ERROR:",
                        e
                    )

            # =========================
            # FUTURE
            # =========================
            future_score = 50

            # =========================
            # WEIGHTS
            # =========================
            weights = (
                self.learning
                .weights()
            )

            # =========================
            # FINAL SCORE
            # =========================
            final = (
                market_score * weights["market"] +
                tech_score * weights["tech"] +
                inst_score * weights["inst"] +
                future_score * weights["future"]
            )

            # =========================
            # MOMENTUM
            # =========================
            close = df["Close"]

            momentum = (
                close.iloc[-1] -
                close.iloc[-20]
            ) / close.iloc[-20]

            if momentum > 0.20:

                final += 20

            elif momentum > 0.10:

                final += 10

            # =========================
            # BREAKOUT
            # =========================
            high50 = df["HIGH50"].iloc[-2]

            if close.iloc[-1] > high50:

                final += 15

            # =========================
            # RETURN
            # =========================
            return {

                "code": code,

                "score": float(final),

                "price": float(
                    close.iloc[-1]
                ),

                "factors": {

                    "market": market_score,

                    "tech": tech_score,

                    "inst": inst_score,

                    "future": future_score
                }
            }

        except Exception as e:

            if self.debug:

                print(
                    "EVALUATE ERROR:",
                    code,
                    e
                )

            return None

    # =====================================================
    # MAIN
    # =====================================================
    def run(self):

        start_year, end_year = (
            self.random_period()
        )

        print("\n========================")
        print("WALK FORWARD TEST")
        print(start_year, "-", end_year)
        print("========================\n")

        # =====================================================
        # SAMPLE
        # =====================================================
        sample = list(
            self.data_map.values()
        )[0]

        sample = sample[
            (sample["Date"].dt.year >= start_year) &
            (sample["Date"].dt.year <= end_year)
        ]

        # =====================================================
        # INDEX MODE
        # =====================================================
        max_days = len(sample)

        # =====================================================
        # PORTFOLIO
        # =====================================================
        cash = self.initial_cash

        positions = {}

        trade_logs = []

        equity_curve = []

        peak = cash

        dd_curve = []

        # =====================================================
        # MAIN LOOP
        # =====================================================
        for day in range(
            self.min_history,
            max_days
        ):

            # =========================
            # FAST LOG
            # =========================
            if day % 20 == 0:

                print(
                    "DAY:",
                    day,
                    "CASH:",
                    int(cash),
                    "POS:",
                    len(positions)
                )

            # =================================================
            # SLICE
            # =================================================
            sliced = self.slice_data(day)

            # =================================================
            # AI
            # =================================================
            candidates = []

            for item in sliced.items():

                r = self.evaluate_code(item)

                if r is not None:

                    candidates.append(r)

            # =================================================
            # SORT
            # =================================================
            candidates = sorted(
                candidates,
                key=lambda x: x["score"],
                reverse=True
            )

            # =================================================
            # SELL
            # =================================================
            remove_codes = []

            for code, pos in positions.items():

                try:

                    if code not in sliced:
                        continue

                    df = sliced[code]

                    current_price = float(
                        df["Close"].iloc[-1]
                    )

                    pnl = (
                        current_price -
                        pos["entry"]
                    ) / pos["entry"]

                    should_exit, reason = (
                        self.exit_manager
                        .should_exit(
                            df=df,
                            entry_price=pos["entry"],
                            current_price=current_price,
                            code=code,
                            confidence=pos["score"]
                        )
                    )

                    if should_exit:

                        amount = (
                            pos["shares"] *
                            current_price
                        )

                        cash += amount

                        trade_logs.append({

                            "type": "SELL",

                            "code": code,

                            "pnl": pnl,

                            "reason": reason
                        })

                        self.learning.update(
                            pos["factors"],
                            pnl
                        )

                        remove_codes.append(code)

                except:
                    continue

            for code in remove_codes:

                del positions[code]

            # =================================================
            # BUY
            # =================================================
            for c in candidates[:self.top_n]:

                try:

                    code = c["code"]

                    if code in positions:
                        continue

                    if len(positions) >= self.max_positions:
                        break

                    # =====================
                    # FILTER
                    # =====================
                    if c["score"] < self.entry_threshold:
                        continue

                    # =====================
                    # POSITION SIZE
                    # =====================
                    score = min(
                        c["score"],
                        100
                    )

                    ratio = (
                        score / 100
                    ) * 0.25

                    allocation = (
                        cash * ratio
                    )

                    if allocation <= 0:
                        continue

                    shares = (
                        allocation /
                        c["price"]
                    )

                    positions[code] = {

                        "shares": shares,

                        "entry": c["price"],

                        "score": score,

                        "factors": c["factors"]
                    }

                    cash -= allocation

                    trade_logs.append({

                        "type": "BUY",

                        "code": code,

                        "price": c["price"]
                    })

                except:
                    continue

            # =================================================
            # EQUITY
            # =================================================
            total = cash

            for code, pos in positions.items():

                try:

                    if code not in sliced:
                        continue

                    price = float(
                        sliced[code]["Close"]
                        .iloc[-1]
                    )

                    total += (
                        pos["shares"] *
                        price
                    )

                except:
                    continue

            equity_curve.append(total)

            peak = max(
                peak,
                total
            )

            dd = (
                peak - total
            ) / peak

            dd_curve.append(dd)

        # =====================================================
        # FINAL
        # =====================================================
        final = equity_curve[-1]

        cagr = (
            (
                final /
                self.initial_cash
            ) ** (1 / 10)
        ) - 1

        max_dd = max(dd_curve)

        print("\n========================")
        print("FINAL:", int(final))
        print(
            "CAGR:",
            round(cagr * 100, 2),
            "%"
        )
        print(
            "MAX DD:",
            round(max_dd * 100, 2),
            "%"
        )
        print(
            "TRADES:",
            len(trade_logs)
        )
        print("========================")

        # =====================================================
        # SAVE GRAPH
        # =====================================================
        plt.figure(figsize=(16, 8))

        plt.plot(equity_curve)

        plt.title(
            f"WalkForward "
            f"{start_year}-{end_year}"
        )

        plt.xlabel("Days")

        plt.ylabel("Portfolio")

        plt.grid(True)

        plt.savefig(
            "equity_curve.png"
        )

        plt.close()

        # =====================================================
        # DD GRAPH
        # =====================================================
        plt.figure(figsize=(16, 5))

        plt.plot(dd_curve)

        plt.title("Drawdown")

        plt.grid(True)

        plt.savefig(
            "drawdown_curve.png"
        )

        plt.close()

        return {

            "final": final,

            "cagr": cagr,

            "max_dd": max_dd,

            "trades": len(trade_logs)
        }


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":

    engine = WalkForwardEngine()

    engine.run()