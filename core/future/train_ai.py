# core/future/train_ai.py

import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import RandomForestClassifier


class TrainAI:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(self):

        self.model = RandomForestClassifier(

            n_estimators=200,

            max_depth=8,

            random_state=42
        )

    # =====================================================
    # LOAD
    # =====================================================
    def load_data(self):

        try:

            df = pd.read_csv(
                "learning_history.csv"
            )

            df = df.dropna()

            return df

        except Exception as e:

            print(
                "LOAD ERROR:",
                e
            )

            return None

    # =====================================================
    # FEATURE ENGINEERING
    # =====================================================
    def create_features(
        self,
        df
    ):

        try:

            # =============================================
            # RETURN
            # =============================================
            df["return_5"] = (
                df["Price"]
                .pct_change(5)
            )

            df["return_20"] = (
                df["Price"]
                .pct_change(20)
            )

            # =============================================
            # MA
            # =============================================
            df["ma5"] = (
                df["Price"]
                .rolling(5)
                .mean()
            )

            df["ma20"] = (
                df["Price"]
                .rolling(20)
                .mean()
            )

            df["ma50"] = (
                df["Price"]
                .rolling(50)
                .mean()
            )

            # =============================================
            # MA DIFF
            # =============================================
            df["ma_diff"] = (

                df["ma5"] -
                df["ma20"]

            ) / df["ma20"]

            # =============================================
            # VOLATILITY
            # =============================================
            df["volatility"] = (

                df["Price"]
                .pct_change()
                .rolling(20)
                .std()

            )

            # =============================================
            # VOLUME POWER
            # =============================================
            df["vol_ratio"] = (

                df["Volume"] /

                df["Volume"]
                .rolling(20)
                .mean()

            )

            # =============================================
            # FUTURE RETURN
            # =============================================
            df["future_return"] = (

                df["Price"]
                .shift(-5) -

                df["Price"]

            ) / df["Price"]

            # =============================================
            # TARGET
            # =============================================
            df["target"] = (
                df["future_return"] > 0.03
            ).astype(int)

            df = df.dropna()

            return df

        except Exception as e:

            print(
                "FEATURE ERROR:",
                e
            )

            return None

    # =====================================================
    # TRAIN
    # =====================================================
    def train(self):

        try:

            df = self.load_data()

            if df is None:

                return

            df = self.create_features(df)

            if df is None:

                return

            if len(df) < 200:

                print("DATA SHORT")

                return

            # =============================================
            # FEATURES
            # =============================================
            features = [

                "Price",

                "Volume",

                "Change",

                "News",

                "return_5",

                "return_20",

                "ma_diff",

                "volatility",

                "vol_ratio"
            ]

            X = df[features]

            y = df["target"]

            # =============================================
            # TRAIN
            # =============================================
            self.model.fit(X, y)

            # =============================================
            # SAVE
            # =============================================
            joblib.dump(
                self.model,
                "model.pkl"
            )

            print(
                "MODEL TRAINED"
            )

            print(
                "ROWS:",
                len(df)
            )

        except Exception as e:

            print(
                "TRAIN ERROR:",
                e
            )


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":

    TrainAI().train()