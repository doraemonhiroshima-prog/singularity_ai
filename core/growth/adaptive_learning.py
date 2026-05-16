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

    self.data = self.load()

# =========================
# LOAD
# =========================
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

# =========================
# SAVE
# =========================
def save(self):

    with open(self.path, "w") as f:

        json.dump(
            self.data,
            f,
            indent=4
        )

# =========================
# CURRENT
# =========================
def weights(self):

    return self.data["weights"]

# =========================
# UPDATE RESULT
# =========================
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

# =========================
# OPTIMIZE
# =========================
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

            score = max(score, 0.01)

        new_weights[k] = score

        total += score

    # 正規化
    for k in new_weights:

        new_weights[k] = (
            new_weights[k] / total
        )

    self.data["weights"] = new_weights

    print("\n=== ADAPTIVE UPDATE ===")

    for k, v in new_weights.items():

        print(
            k,
            round(v, 3)
        )

