import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib


class TrainAI:

    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)

    def load_data(self):

        try:
            df = pd.read_csv("learning_history.csv")  # ←自動化OK

            # 必要列だけ
            df = df[["Price", "Volume", "Change", "News"]]

            df = df.dropna()

            return df

        except Exception as e:
            print("LOAD ERROR:", e)
            return None

    def create_label(self, df):

        # 未来リターン（次の値）
        df["future"] = df["Price"].shift(-5)

        # 上昇したか（分類）
        df["target"] = (df["future"] > df["Price"]).astype(int)

        df = df.dropna()

        return df

    def train(self):

        df = self.load_data()

        if df is None or len(df) < 100:
            print("データ不足")
            return

        df = self.create_label(df)

        X = df[["Price", "Volume", "Change", "News"]]
        y = df["target"]

        self.model.fit(X, y)

        joblib.dump(self.model, "model.pkl")

        print("✅ MODEL TRAINED & SAVED")


if __name__ == "__main__":
    TrainAI().train()
