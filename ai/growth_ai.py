import json
import random

from core.growth.evaluator import Evaluator


class GrowthAI:

    def __init__(self, path="config.json"):

        self.path = path
        self.evaluator = Evaluator()

    def run(self, results):

        # =========================
        # 評価
        # =========================
        metrics = self.evaluator.evaluate(results)

        # =========================
        # 設定ロード
        # =========================
        try:
            with open(self.path, "r") as f:
                config = json.load(f)

        except:
            config = {
                "score_threshold": 60,
                "take_profit": 0.15,
                "stop_loss": 0.05
            }

        # =========================
        # 学習
        # =========================
        acc5 = metrics["acc5"]

        if acc5 < 0.5:

            config["score_threshold"] += random.randint(-2, 2)

        else:

            config["take_profit"] += random.uniform(-0.01, 0.01)

        # =========================
        # 保存
        # =========================
        with open(self.path, "w") as f:
            json.dump(config, f, indent=2)

        return {
            "metrics": metrics,
            "config": config
        }