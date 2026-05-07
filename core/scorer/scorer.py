class Scorer:

    def calculate(self, data):

        score = 0

        score += data.get("technical", 0) * 0.30
        score += data.get("institution", 0) * 0.25
        score += data.get("news", 0) * 0.10
        score += data.get("future", 0) * 0.25
        score += data.get("market", 0) * 0.10

        return round(score, 2)