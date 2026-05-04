import json


class StrategyAI:

    def __init__(self):
        try:
            with open("config.json", "r") as f:
                self.config = json.load(f)
        except:
            self.config = {}

    def select(self, signals):

        if not signals:
            return []

        threshold = self.config.get("score_threshold", 120)
        max_positions = self.config.get("max_positions", 5)

        # confidence高い順
        signals = sorted(
            signals,
            key=lambda x: x["confidence"],
            reverse=True
        )

        selected = []

        for s in signals:
            if s["confidence"] >= threshold:
                selected.append(s)

            if len(selected) >= max_positions:
                break

        # fallback
        if not selected:
            selected = signals[:max_positions]

        return selected
