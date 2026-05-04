from make_stock_list import create_stock_list
from ai.market_scan.market_scan_ai import MarketScanAI
from ai.technical.technical_runner import TechnicalAI
from news.news_ai import NewsAI
from ai.institution.institution_ai import InstitutionAI
from news.theme_detector import ThemeDetector
import numpy as np


class PipelineController:

    def __init__(self):

        self.UPDATE_STOCK_LIST = False

        self.market_ai = MarketScanAI()
        self.technical_ai = TechnicalAI()
        self.news_ai = NewsAI()
        self.inst_ai = InstitutionAI()
        self.theme = ThemeDetector()

    def run(self):

        print("=== PIPELINE START ===")

        if self.UPDATE_STOCK_LIST:
            create_stock_list()

        # =========================
        # Market
        # =========================
        market_data = self.market_ai.process()

        # =========================
        # Technical
        # =========================
        tech_data = self.technical_ai.process(market_data)

        results = []
        theme_scores = []

        # =========================
        # 一旦スコア作成
        # =========================
        for r in tech_data:

            try:
                news = self.news_ai.analyze(r["code"], r["name"])
                inst = self.inst_ai.analyze(r["df"])

                theme_score, matched = self.theme.analyze(r["name"])

                total = (
                    r["market_score"] +
                    r["technical_score"] +
                    news["score"] +
                    inst +
                    theme_score
                )

                results.append({
                    "code": r["code"],
                    "name": r["name"],
                    "total": total,
                    "M": r["market_score"],
                    "T": r["technical_score"],
                    "N": news["score"],
                    "I": inst,
                    "TH": theme_score,
                    "themes": matched
                })

                theme_scores.append(theme_score)

            except:
                continue

        # =========================
        # 🔥 セクター資金（重要）
        # =========================
        avg_theme = np.mean(theme_scores) if theme_scores else 0

        for r in results:

            # テーマ強い銘柄に追加加点
            if r["TH"] > avg_theme:
                r["total"] += 30

        # =========================
        # フィルタ
        # =========================
        results = sorted(results, key=lambda x: x["total"], reverse=True)

        print("\n=== FINAL ===")
        for i, r in enumerate(results[:10]):
            print(f"{i+1}: {r['code']} TOTAL:{r['total']}")

        return results
