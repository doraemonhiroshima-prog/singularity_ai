from core.technical.indicators import Indicators
from core.technical.breakout_detector import BreakoutDetector


class TechnicalAI:

    def __init__(self):

        self.indicator = Indicators()

        self.breakout = BreakoutDetector()

    def run(self, df):

        score1 = self.indicator.calculate(df)

        score2 = self.breakout.detect(df)

        total = (
            score1 * 0.6 +
            score2 * 0.4
        )

        return max(
            min(total, 100),
            0
        )