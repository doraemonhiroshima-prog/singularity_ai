    # core/signal/signals.py


class SignalGenerator:

    def generate(
        self,
        data,
        weights,
        threshold
    ):

        try:

            score = (
                float(data["market"]) *
                float(weights["market"])

                +

                float(data["tech"]) *
                float(weights["tech"])

                +

                float(data["news"]) *
                float(weights["news"])

                +

                float(data["inst"]) *
                float(weights["inst"])

                +

                float(data["future"]) *
                float(weights["future"])
            )

            print(
                "SIGNAL SCORE:",
                round(score, 2),
                "THRESHOLD:",
                threshold
            )

            # 一時的にかなり緩くする
            if score >= 30:

                print("BUY GENERATED")

                return {
                    "signal": "BUY",
                    "confidence": round(score, 2)
                }

            return {
                "signal": "NONE",
                "confidence": round(score, 2)
            }

        except Exception as e:

            print(
                "SIGNAL ERROR:",
                e
            )

            return {
                "signal": "NONE",
                "confidence": 0
            }