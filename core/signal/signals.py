import json


class SignalGenerator:

    def __init__(self):
        try:
            with open("config.json", "r") as f:
                self.config = json.load(f)
        except:
            self.config = {}

    def generate(self, data):

        # 🔥 強いトレンドのみ
        if data["future"] < 60:
            return {"signal": "NONE", "confidence": 0}

        score = (
            data["future"] * 0.7 +
            data["tech"] * 0.2 +
            data["inst"] * 0.1
        )

        threshold = self.config.get("score_threshold", 70)

        if score >= threshold:
            return {
                "signal": "BUY",
                "confidence": score
            }

        return {
            "signal": "NONE",
            "confidence": score
        }
