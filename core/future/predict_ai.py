from core.future.predict_ai import PredictAI
from core.future.crash_detector import CrashDetector


class FuturePredictionAI:

    def __init__(self):

        self.predict_ai = PredictAI()
        self.crash = CrashDetector()

    def run(self, df):

        try:

            future_score = self.predict_ai.predict(df)

        except:

            future_score = 50

        try:

            crash = self.crash.detect(df)

        except:

            crash = 0

        future_score = max(future_score - crash, 0)

        return {
            "score": future_score,
            "crash": crash
        }