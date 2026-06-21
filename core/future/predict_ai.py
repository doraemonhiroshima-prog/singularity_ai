# core/future/predict_ai.py

import numpy as np
import pandas as pd
import joblib
import os


class PredictAI:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(self):

        self.model = None

        try:

            if os.path.exists("model.pkl"):

                self.model = joblib.load(
                    "model.pkl"
                )

                print(
                    "MODEL LOADED"
                )

        except Exception as e:

            print(
                "MODEL LOAD ERROR:",
                e
            )

    # =====================================================
    # CREATE FEATURES
    # =====================================================
    def create_features(
        self,
        df
    ):

        close = df["Close"]

        price = close.iloc[-1]

        volume = (
            df["Volume"]
            .iloc[-1]
        )

        change = (

            close.iloc[-1] -
            close.iloc[-2]

        ) / close.iloc[-2]

        news = 50

        return_5 = (
            close
            .pct_change(5)
            .iloc[-1]
        )

        return_20 = (
            close
            .pct_change(20)
            .iloc[-1]
        )

        ma5 = (
            close
            .rolling(5)
            .mean()
            .iloc[-1]
        )

        ma20 = (
            close
            .rolling(20)
            .mean()
            .iloc[-1]
        )

        ma_diff = (
            ma5 - ma20
        ) / ma20

        volatility = (

            close
            .pct_change()
            .rolling(20)
            .std()
            .iloc[-1]
        )

        vol_ratio = (

            volume /

            df["Volume"]
            .rolling(20)
            .mean()
            .iloc[-1]

        )

        X = pd.DataFrame([{

            "Price": price,

            "Volume": volume,

            "Change": change,

            "News": news,

            "return_5": return_5,

            "return_20": return_20,

            "ma_diff": ma_diff,

            "volatility": volatility,

            "vol_ratio": vol_ratio
        }])

        return X

    # =====================================================
    # PREDICT
    # =====================================================
    def predict(
        self,
        df
    ):

        try:

            if len(df) < 80:

                return {

                    "score": 50,

                    "expected_return": 0,

                    "volatility": 0,

                    "momentum": 0
                }

            close = df["Close"]

            momentum = (

                close.iloc[-1] -
                close.iloc[-20]

            ) / close.iloc[-20]

            volatility = (

                close
                .pct_change()
                .rolling(20)
                .std()
                .iloc[-1]
            )

            expected_return = momentum

            # =============================================
            # ML MODEL
            # =============================================
            ml_score = 50

            if self.model is not None:

                X = self.create_features(df)

                prob = (
                    self.model
                    .predict_proba(X)[0][1]
                )

                ml_score = prob * 100

            # =============================================
            # RULE BOOST
            # =============================================
            ma5 = (
                close
                .rolling(5)
                .mean()
                .iloc[-1]
            )

            ma20 = (
                close
                .rolling(20)
                .mean()
                .iloc[-1]
            )

            if ma5 > ma20:

                ml_score += 10

            else:

                ml_score -= 10

            # =============================================
            # NORMALIZE
            # =============================================
            ml_score = max(
                min(ml_score, 100),
                0
            )

            return {

                "score": float(ml_score),

                "expected_return": float(
                    expected_return
                ),

                "volatility": float(
                    volatility
                ),

                "momentum": float(
                    momentum
                )
            }

        except Exception as e:

            print(
                "PREDICT ERROR:",
                e
            )

            return {

                "score": 50,

                "expected_return": 0,

                "volatility": 0,

                "momentum": 0
            }