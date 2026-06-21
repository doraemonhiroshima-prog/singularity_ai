# core/growth/adaptive_learning.py

import json
import os
import numpy as np


class AdaptiveLearning:

    def __init__(self):

        self.path = "learning_result.json"

        self.default_weights = {

            "market": 0.15,

            "tech": 0.40,

            "news": 0.10,

            "inst": 0.15,

            "future": 0.20
        }

        # =========================================
        # MAX CHANGE LIMIT
        # =========================================
        self.max_change = 0.03

        self.data = self.load()

    # =============================================
    # LOAD
    # =============================================
    def load(self):

        if not os.path.exists(self.path):

            return {

                "weights": self.default_weights,

                "history": []
            }

        try:

            with open(self.path, "r") as f:

                return json.load(f)

        except:

            return {

                "weights": self.default_weights,

                "history": []
            }

    # =============================================
    # SAVE
    # =============================================
    def save(self):

        with open(self.path, "w") as f:

            json.dump(
                self.data,
                f,
                indent=4
            )

    # =============================================
    # CURRENT WEIGHTS
    # =============================================
    def weights(self):

        return self.data["weights"]

    # =============================================
    # UPDATE
    # =============================================
    def update(

        self,
        factors,
        profit
    ):

        try:

            self.data["history"].append({

                "factors": factors,

                "profit": float(profit)
            })

            # 履歴制限
            self.data["history"] = (
                self.data["history"][-300:]
            )

            self.optimize()

            self.save()

        except Exception as e:

            print(
                "LEARNING ERROR:",
                e
            )

    # =============================================
    # OPTIMIZE
    # =============================================
    def optimize(self):

        history = self.data["history"]

        if len(history) < 30:
            return

        scores = {

            "market": [],

            "tech": [],

            "news": [],

            "inst": [],

            "future": []
        }

        for h in history:

            profit = h["profit"]

            for k, v in h["factors"].items():

                if k not in scores:
                    continue

                scores[k].append(
                    v * profit
                )

        new_weights = {}

        total = 0

        for k, vals in scores.items():

            if len(vals) == 0:

                score = 1

            else:

                score = (

                    np.mean(vals) * 0.3

                ) + (

                    self.default_weights[k] * 100
                )

                score = max(
                    score,
                    0.01
                )

            new_weights[k] = score

            total += score

        # =========================================
        # NORMALIZE
        # =========================================
        for k in new_weights:

            new_weights[k] = (
                new_weights[k] / total
            )

        # =========================================
        # ANTI OVERFIT LIMIT
        # =========================================
        current = self.data["weights"]

        limited = {}

        for k in new_weights:

            old = current.get(
                k,
                self.default_weights[k]
            )

            new = new_weights[k]

            diff = new - old

            if diff > self.max_change:

                new = (
                    old +
                    self.max_change
                )

            elif diff < -self.max_change:

                new = (
                    old -
                    self.max_change
                )

            limited[k] = new

        # =========================================
        # RE NORMALIZE
        # =========================================
        total = sum(
            limited.values()
        )

        for k in limited:

            limited[k] = (
                limited[k] / total
            )

        self.data["weights"] = limited

        print("\n=== ADAPTIVE UPDATE ===")

        for k, v in limited.items():

            print(
                k,
                round(v, 3)
            )