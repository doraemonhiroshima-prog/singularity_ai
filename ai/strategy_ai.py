from core.strategy.market_regime import MarketRegime
from core.strategy.adaptive_weights import AdaptiveWeights
from core.strategy.auto_tuner import AutoTuner
from core.strategy.winrate_learning import WinRateLearning


class StrategyAI:

    def __init__(self):

        self.regime = MarketRegime()

        self.weights = AdaptiveWeights()

        self.tuner = AutoTuner()

        self.learning = WinRateLearning()

    def build(self, df):

        regime = self.regime.detect(df)

        weights = self.weights.get(regime)

        winrate = self.learning.rate()

        threshold = self.tuner.threshold(
            winrate
        )

        return {
            "regime": regime,
            "weights": weights,
            "threshold": threshold,
            "winrate": winrate
        }

    def update(self, profit):

        self.learning.update(profit)