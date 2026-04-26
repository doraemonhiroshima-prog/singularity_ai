import joblib
import pandas as pd
import numpy as np
import os


class PredictAI:

    def __init__(self):

        if os.path.exists("model.pkl"):
            self.model = joblib.load("model.pkl")
        else:
            print("⚠ modelなし → 仮モード")
            self.model = None

    # =========================
    # 確率予測
    # =========================
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

    # =========================
    # 未来シミュレーション
    # =========================
    def process(self, df):

        try:
            close = df["Close"]

            if len(close) < 50:
                return {"future_score": 50}

            price = float(close.iloc[-1])
            volume = float(df["Volume"].iloc[-1])
            change = float(close.pct_change().iloc[-1])

            # ★ 既存AI
            prob = self.predict(price, volume, change, 0)

            # =========================
            # モンテカルロ
            # =========================
            sims = []

            for _ in range(30):
                p = price

                for _ in range(20):

                    if np.random.rand() < prob:
                        c = np.random.normal(0.005, 0.02)
                    else:
                        c = np.random.normal(-0.003, 0.02)

                    p *= (1 + c)

                sims.append(p)

            sims = np.array(sims)

            up_prob = np.mean(sims > price)

            return {
                "future_score": float(up_prob * 100),
                "prob": float(prob),
                "mean_future": float(np.mean(sims)),
                "max_future": float(np.max(sims)),
                "min_future": float(np.min(sims))
            }

        except Exception as e:
            print("FutureAI ERROR:", e)
            return {"future_score": 50}
