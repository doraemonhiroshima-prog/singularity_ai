# 改良版 core/growth/evaluator.py

import os
import pandas as pd
import numpy as np

class Evaluator:


 def evaluate(self, results):

    hit_1 = 0
    hit_5 = 0
    hit_10 = 0

    total = 0

    profits = []

    equity = 1000000

    peak = equity

    max_dd = 0

    wins = 0

    losses = 0

    for r in results:

        try:

            path = f"data/{r['code']}.csv"

            if not os.path.exists(path):
                continue

            df = pd.read_csv(path)

            if len(df) < 15:
                continue

            close = df["Close"]

            base = float(close.iloc[-11])

            p1 = float(close.iloc[-10])

            p5 = float(close.iloc[-6])

            p10 = float(close.iloc[-1])

            # =========================
            # HIT
            # =========================
            if p1 > base:
                hit_1 += 1

            if p5 > base:
                hit_5 += 1

            if p10 > base:
                hit_10 += 1

            # =========================
            # RETURN
            # =========================
            ret = (
                p5 - base
            ) / base

            profits.append(ret)

            if ret > 0:

                wins += 1

            else:

                losses += 1

            equity *= (1 + ret)

            peak = max(
                peak,
                equity
            )

            dd = (
                peak - equity
            ) / peak

            max_dd = max(
                max_dd,
                dd
            )

            total += 1

        except:

            continue

    # =========================
    # METRICS
    # =========================
    acc1 = hit_1 / total if total else 0

    acc5 = hit_5 / total if total else 0

    acc10 = hit_10 / total if total else 0

    avg_profit = (
        np.mean(profits)
        if profits else 0
    )

    std = (
        np.std(profits)
        if profits else 0
    )

    sharpe = (
        avg_profit / std
        if std > 0 else 0
    )

    pf = (
        wins / losses
        if losses > 0 else wins
    )

    print("\n=== EVALUATION ===")

    print(
        "1D WIN:",
        round(acc1, 3)
    )

    print(
        "5D WIN:",
        round(acc5, 3)
    )

    print(
        "10D WIN:",
        round(acc10, 3)
    )

    print(
        "AVG PROFIT:",
        round(avg_profit, 4)
    )

    print(
        "MAX DD:",
        round(max_dd, 4)
    )

    print(
        "SHARPE:",
        round(sharpe, 3)
    )

    print(
        "PF:",
        round(pf, 3)
    )

    return {

        "acc1": acc1,

        "acc5": acc5,

        "acc10": acc10,

        "profit": avg_profit,

        "dd": max_dd,

        "sharpe": sharpe,

        "pf": pf
    }

