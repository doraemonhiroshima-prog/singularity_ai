# core/market_scan/pipeline_controller.py

from core.market_scan.market_regime import (
    MarketRegime
)

from core.market_scan.market_ranker import (
    MarketRanker
)


class PipelineController:

    def __init__(self):

        self.regime = (
            MarketRegime()
        )

        self.ranker = (
            MarketRanker()
        )

    def run(
        self,
        df
    ):

        regime = (
            self.regime.analyze(df)
        )

        score = (
            self.ranker.score(
                df,
                regime
            )
        )

        return {

            "score": score,

            "regime":
                regime.get(
                    "regime",
                    "SIDE"
                )
        }