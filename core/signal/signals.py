class SignalGenerator:

    def generate(self, data, weights, threshold):

        score = (
            data["market"] * weights["market"] +
            data["tech"] * weights["tech"] +
            data["news"] * weights["news"] +
            data["inst"] * weights["inst"] +
            data["future"] * weights["future"]
        )

        if score >= threshold:

            return {
                "signal": "BUY",
                "confidence": score
            }

        return {
            "signal": "NONE",
            "confidence": score
        }