import json
import random


class GrowthAI:

    def __init__(self, path="config.json"):
        self.path = path

    def evolve(self, score):

        with open(self.path, "r") as f:
            config = json.load(f)

        if score < 1.0:
            config["score_threshold"] += random.randint(-2, 2)
        else:
            config["take_profit"] += random.uniform(-0.01, 0.01)

        with open(self.path, "w") as f:
            json.dump(config, f, indent=2)