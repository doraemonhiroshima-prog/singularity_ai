import pandas as pd
import numpy as np
from .predict_ai import PredictAI


class FuturePredictionAI:

    def __init__(self):
        self.predictor = PredictAI()

    def _simulate_path(self, price, prob, steps=20):
        """
        簡易モンテカルロ
        """
        prices = [price]

        for _ in range(steps):

            # 上昇確率で分岐
            if np.random.rand() < prob:
                change = np.random.normal(0.005, 0.02)  # 上昇寄り
            else:
                change = np.random.normal(-0.003, 0.02)

            price = price * (1 + change)
            prices.append(price)

        return prices

    def _multi_simulation(self, price, prob, runs=50):
        paths = []

        for _ in range(runs):
            path = self._simulate_path(price, prob)
            paths.append(path)

        return np.array(paths)

    def process(self, df):

        try:
            price = float(df["Close"].iloc[-1])
            volume = float(df["Volume"].iloc[-1])
            change = float(df["Close"].pct_change().iloc[-1])

            # ★ 既存AI
            prob = self.predictor.predict(price, volume, change, 0)

            # =========================
            # シミュレーション
            # =========================
            sims = self._multi_simulation(price, prob)

            # =========================
            # 統計
            # =========================
            final_prices = sims[:, -1]

            mean_price = np.mean(final_prices)
            max_price = np.max(final_prices)
            min_price = np.min(final_prices)

            # 上昇確率（現在価格より上）
            up_prob = np.mean(final_prices > price)

            # スコア化
            score = up_prob * 100

            return {
                "prob": prob,
                "future_score": score,
                "mean_price": mean_price,
                "max_price": max_price,
                "min_price": min_price
            }

        except Exception as e:
            print("FutureAI ERROR:", e)
            return {
                "prob": 0.5,
                "future_score": 50
            }
