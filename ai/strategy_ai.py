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

        # =========================
        # 相場判定
        # =========================
        regime = self.regime.detect(df)

        # =========================
        # AI重み
        # =========================
        weights = self.weights.get(regime)

        # =========================
        # 学習勝率
        # =========================
        winrate = self.learning.rate()

        # =========================
        # 自動threshold
        # =========================
        threshold = self.tuner.threshold(
            winrate=winrate,
            signal_count=10,
            regime=regime
        )

        return {
            "regime": regime,
            "weights": weights,
            "threshold": threshold,
            "winrate": winrate
        }

    def update(self, profit):

        self.learning.update(profit)