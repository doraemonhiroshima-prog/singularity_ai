# ai/strategy_ai.py

from core.strategy.adaptive_weights import AdaptiveWeights
from core.strategy.auto_tuner import AutoTuner
from core.strategy.winrate_learning import WinRateLearning

from core.market_scan.market_regime import MarketRegime


class StrategyAI:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(self):

        self.regime = MarketRegime()

        self.weights = AdaptiveWeights()

        self.tuner = AutoTuner()

        self.learning = WinRateLearning()

    # =====================================================
    # BUILD
    # =====================================================
    def build(
        self,
        df
    ):

        try:

            # =============================================
            # REGIME
            # =============================================
            regime_data = (
                self.regime
                .analyze(df)
            )

            regime = (
                regime_data["regime"]
            )

            regime_score = (
                regime_data["score"]
            )

            # =============================================
            # WEIGHTS
            # =============================================
            weights = (
                self.weights
                .get(regime)
            )

            # =============================================
            # WINRATE
            # =============================================
            winrate = (
                self.learning
                .rate()
            )

            # =============================================
            # THRESHOLD
            # =============================================
            threshold = (
                self.tuner
                .threshold(
                    winrate=winrate,
                    signal_count=10,
                    regime=regime
                )
            )

            # =============================================
            # RETURN
            # =============================================
            return {

                "regime": regime,

                "regime_score": regime_score,

                "weights": weights,

                "threshold": threshold,

                "winrate": winrate
            }

        except Exception as e:

            print(
                "STRATEGY AI ERROR:",
                e
            )

            return {

                "regime": "SIDE",

                "regime_score": 50,

                "weights": {

                    "market": 0.2,

                    "tech": 0.4,

                    "inst": 0.2,

                    "future": 0.2
                },

                "threshold": 50,

                "winrate": 0.5
            }

    # =====================================================
    # UPDATE
    # =====================================================
    def update(
        self,
        profit
    ):

        try:

            self.learning.update(
                profit
            )

        except Exception as e:

            print(
                "STRATEGY UPDATE ERROR:",
                e
            )