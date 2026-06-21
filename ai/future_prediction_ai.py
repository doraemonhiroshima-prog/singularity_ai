# ai/future_prediction_ai.py

from core.future.predict_ai import PredictAI
from core.future.crash_detector import CrashDetector
from core.future.train_ai import TrainAI


class FuturePredictionAI:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(self):

        self.predict_ai = PredictAI()

        self.crash_detector = CrashDetector()

        # 学習AIは将来用
        self.train_ai = TrainAI()

    # =====================================================
    # NORMALIZE
    # =====================================================
    def normalize(self, value):

        try:

            if isinstance(value, dict):

                if "score" in value:
                    return float(value["score"])

                return 50.0

            return float(value)

        except:

            return 50.0

    # =====================================================
    # RUN
    # =====================================================
    def run(self, df):

        try:

            if len(df) < 80:
                return 50

            # =============================================
            # PREDICT
            # =============================================
            predict_score = (
                self.predict_ai
                .predict(df)
            )

            predict_score = (
                self.normalize(
                    predict_score
                )
            )

            # =============================================
            # CRASH
            # =============================================
            crash_score = (
                self.crash_detector
                .detect(df)
            )

            crash_score = (
                self.normalize(
                    crash_score
                )
            )

            # =============================================
            # START
            # =============================================
            score = predict_score

            # =============================================
            # CRASH PENALTY
            # =============================================
            score -= (
                crash_score * 0.5
            )

            # =============================================
            # MOMENTUM
            # =============================================
            close = df["Close"]

            momentum = (

                close.iloc[-1] -
                close.iloc[-20]

            ) / close.iloc[-20]

            score += (
                momentum * 100
            )

            # =============================================
            # VOLATILITY
            # =============================================
            returns = (
                close.pct_change()
            )

            volatility = (
                returns.tail(20).std()
            )

            score -= (
                volatility * 120
            )

            # =============================================
            # NORMALIZE
            # =============================================
            score = max(
                min(score, 100),
                0
            )

            return float(score)

        except Exception as e:

            print(
                "FUTURE AI ERROR:",
                e
            )

            return 50