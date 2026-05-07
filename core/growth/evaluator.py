import os
import pandas as pd


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

        for r in results[:20]:

            path = f"data/{r['code']}.csv"

            if not os.path.exists(path):
                continue

            df = pd.read_csv(path)

            if len(df) < 15:
                continue

            if "Close" not in df.columns:
                df.columns = ["Date","Close","High","Low","Open","Volume"]

            close = df["Close"]

            try:
                base = float(close.iloc[-11])
                p1 = float(close.iloc[-10])
                p5 = float(close.iloc[-6])
                p10 = float(close.iloc[-1])

                # =========================
                # 勝率
                # =========================
                if p1 > base:
                    hit_1 += 1

                if p5 > base:
                    hit_5 += 1

                if p10 > base:
                    hit_10 += 1

                # =========================
                # 利益
                # =========================
                ret = (p5 - base) / base
                profits.append(ret)

                equity *= (1 + ret)

                # =========================
                # DD
                # =========================
                peak = max(peak, equity)
                dd = (peak - equity) / peak
                max_dd = max(max_dd, dd)

                total += 1

            except:
                continue

        acc1 = hit_1 / total if total else 0
        acc5 = hit_5 / total if total else 0
        acc10 = hit_10 / total if total else 0
        avg_profit = sum(profits) / len(profits) if profits else 0

        print("\n=== 評価 ===")
        print("1日勝率:", round(acc1, 3))
        print("5日勝率:", round(acc5, 3))
        print("10日勝率:", round(acc10, 3))
        print("平均利益:", round(avg_profit, 4))
        print("最大DD:", round(max_dd, 3))

        return {
            "acc1": acc1,
            "acc5": acc5,
            "acc10": acc10,
            "profit": avg_profit,
            "dd": max_dd
        }
