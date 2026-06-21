# ai/market_scan_ai.py

from core.market_scan.market_regime import (
    MarketRegime
)

from core.market_scan.market_ranker import (
    MarketRanker
)


class MarketScanAI:

    def __init__(self):

        self.regime_ai = (
            MarketRegime()
        )

        self.ranker = (
            MarketRanker()
        )

    def run(
        self,
        df
    ):

        try:

            if len(df) < 80:

                return 50

            regime = (
                self.regime_ai
                .analyze(df)
            )

            score = (
                self.ranker
                .score(
                    df,
                    regime
                )
            )

            return float(score)

        except:

            return 50