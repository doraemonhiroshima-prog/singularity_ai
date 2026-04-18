import joblib
import pandas as pd
import os


class PredictAI:

    def __init__(self):

        if os.path.exists("model.pkl"):
            self.model = joblib.load("model.pkl")
        else:
            print("⚠ modelなし → 仮モード")
            self.model = None

    def predict(self, price, volume, change, news):

        if self.model is None:
            return 0.5

        X = pd.DataFrame([{
            "Price": price,
            "Volume": volume,
            "Change": change,
            "News": news
        }])

        return self.model.predict_proba(X)[0][1]
