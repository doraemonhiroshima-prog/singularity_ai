from make_stock_list import create_stock_list
from market_scan.market_scan_ai import MarketScanAI
from technical.technical_runner import TechnicalAI
from news_ai import NewsAI
from institution.institution_ai import InstitutionAI
from growth.growth_ai import GrowthAI

import numpy as np


class PipelineController:

    def __init__(self):

        # ★ 週1だけTrue
        self.UPDATE_STOCK_LIST = False

        self.market_ai = MarketScanAI()
        self.technical_ai = TechnicalAI()
        self.news_ai = NewsAI()
        self.inst_ai = InstitutionAI()
        self.growth_ai = GrowthAI()

    def run(self):

        print("=== PIPELINE START (GROWTH MODE) ===")

        # =========================
        # 銘柄更新
        # =========================
        if self.UPDATE_STOCK_LIST:
            print("銘柄リスト更新中...")
            create_stock_list()

        # =========================
        # Market
        # =========================
        market_data = self.market_ai.process()
        print("[Market]", len(market_data))

        # =========================
        # Technical
        # =========================
        tech_data = self.technical_ai.process(market_data)
        print("[Technical]", len(tech_data))

        results = []

        # =========================
        # 統合処理
        # =========================
        for r in tech_data:

            try:
                news = self.news_ai.analyze(r["code"], r["name"])
                inst = self.inst_ai.analyze(r["df"])
                growth = self.growth_ai.analyze(r["code"])

                total = (
                    r["market_score"] +
                    r["technical_score"] +
                    news["score"] +
                    inst +
                    growth
                )

                results.append({
                    "code": r["code"],
                    "name": r["name"],
                    "total": total,
                    "M": r["market_score"],
                    "T": r["technical_score"],
                    "N": news["score"],
                    "I": inst,
                    "G": growth,
                    "cap": r.get("market_cap", 0)
                })

            except Exception as e:
                print("ERROR:", r.get("code"), e)
                continue

        # =========================
        # データなし対策
        # =========================
        if len(results) == 0:
            print("データなし")
            return []

        # =========================
        # スコア分析
        # =========================
        scores = [r["total"] for r in results]

        avg = np.mean(scores)
        std = np.std(scores)

        threshold = avg + std * 0.3

        print(f"AVG: {avg:.2f} STD: {std:.2f}")
        print(f"THRESHOLD: {threshold:.2f}")

        # =========================
        # フィルタ
        # =========================
        # フィルタ（強化版）
        final = [
            r for r in results
            if r["total"] >= threshold
            and r["T"] >= 0   # ←ここ追加（テクニカル弱いの除外）
]


        if len(final) < 10:
            final = sorted(results, key=lambda x: x["total"], reverse=True)[:20]

        final = sorted(final, key=lambda x: x["total"], reverse=True)

        # =========================
        # 出力
        # =========================
        print("\n=== FINAL RANKING ===")

        for i, r in enumerate(final[:10]):
            print(
                f"{i+1}: {r['code']} | {r['name']} | "
                f"TOTAL:{r['total']:.1f} | "
                f"M:{r['M']} T:{r['T']} N:{r['N']} I:{r['I']} G:{r['G']} | "
                f"CAP:{r['cap']/1e8:.0f}億"
            )

        return final


if __name__ == "__main__":
    PipelineController().run()
