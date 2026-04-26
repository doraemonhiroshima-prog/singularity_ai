class SignalGenerator:

    def generate(self, data):

        T = data.get("T", 0)
        I = data.get("I", 0)
        N = data.get("N", 0)
        F = data.get("F", 50)

        # =========================
        # 🔥 未来フィルター（最重要）
        # =========================
        if F < 70:
            return {
                "signal": "HOLD",
                "confidence": 0
            }

        score = T + I + N + F

        # =========================
        # 判定
        # =========================
        if score > 200:
            return {
                "signal": "BUY",
                "confidence": 0.9
            }

        elif score > 140:
            return {
                "signal": "BUY",
                "confidence": 0.7
            }

        elif score < 80:
            return {
                "signal": "SELL",
                "confidence": 0.8
            }

        return {
            "signal": "HOLD",
            "confidence": 0.5
        }
