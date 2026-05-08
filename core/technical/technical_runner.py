from core.technical.indicators import Indicators
from core.technical.breakout_detector import BreakoutDetector
from core.technical.signals import (
    volume_score,
    breakout_score
)


class TechnicalAI:

    def __init__(self):

        self.indicators = Indicators()
        self.breakout = BreakoutDetector()

    def run(self, df):

        try:

            indicator_score = self.indicators.calculate(df)

            volume = volume_score(df)

            breakout = breakout_score(df)

            breakout_detect = self.breakout.detect(df)

            total = (
                indicator_score +
                volume +
                breakout +
                breakout_detect
            ) / 4

            return {
                "score": round(total, 2),
                "indicator": indicator_score,
                "volume": volume,
                "breakout": breakout
            }

        except Exception as e:

            print("TECH ERROR:", e)

            return {
                "score": 50
            }

    # pipeline_controller互換
    def process(self, market_data):

        results = []

        for item in market_data:

            try:

                df = item["df"]

                tech = self.run(df)

                item["technical_score"] = tech["score"]

                results.append(item)

            except:
                continue

        return results