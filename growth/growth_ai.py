import json
import random


class GrowthAI:

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load()

    def load(self):
        with open(self.config_file, "r") as f:
            return json.load(f)

    def save(self):
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)

    def evolve(self, score):

        print("現在スコア:", score)

        # =========================
        # 改善ロジック
        # =========================
        if score < 1.0:
            print("❌ 負け → 攻め方変更")

            self.config["tech_weight"] += random.uniform(-0.05, 0.05)
            self.config["inst_weight"] += random.uniform(-0.05, 0.05)
            self.config["flow_weight"] += random.uniform(-0.05, 0.05)

            self.config["entry_threshold"] += random.uniform(0.01, 0.05)

        else:
            print("✅ 勝ち → 微調整")

            self.config["take_profit"] += random.uniform(-0.01, 0.01)
            self.config["stop_loss"] += random.uniform(-0.01, 0.01)

        # =========================
        # 制限
        # =========================
        for k in self.config:
            if isinstance(self.config[k], float):
                self.config[k] = max(min(self.config[k], 1), -1)

        self.save()

        print("新パラメータ:", self.config)
