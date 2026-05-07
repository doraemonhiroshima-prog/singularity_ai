# ai/future_prediction_ai.py

from core.future.predict_ai import PredictAI


class FuturePredictionAI:

    def __init__(self):
        self.model = PredictAI()

    def run(self, df):

        if df is None or len(df) < 20:
            return 50

        try:
            price = float(df["Close"].iloc[-1])
            volume = float(df["Volume"].iloc[-1])
            change = float(df["Close"].pct_change().iloc[-1])

            prob = self.model.predict(
                price,
                volume,
                change,
                0
            )

            return prob * 100

        except:
            return 50