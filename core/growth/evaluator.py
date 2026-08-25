# core/growth/evaluator.py

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

        # =========================
        # ACTUAL TRADE RESULTS
        # =========================
        for r in results:

            try:

                ret = float(
                    r.get("profit", 0)
                )
                entry_day = int(
                    r.get("entry_day", 0)
                )

                exit_day = int(
                    r.get("exit_day", 0)
                )
                profits.append(ret)

                if ret > 0:

                    wins += 1

                else:

                    losses += 1

                total += 1

            except:

                continue

        # =========================
        # METRICS
        # =========================

        # 現段階では実際の売買結果を
        # 評価するため、1D/5D/10Dは未使用
        acc1 = 0
        acc5 = 0
        acc10 = 0

        for r in results:

            entry_day = int(
                r.get("entry_day", 0)
            )

            exit_day = int(
                r.get("exit_day", 0)
            )

            days = exit_day - entry_day

            if days >= 1:
                acc1 += 1

            if days >= 5:
                acc5 += 1

            if days >= 10:
                acc10 += 1
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