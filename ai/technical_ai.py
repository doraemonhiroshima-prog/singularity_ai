    #ai/technical_ai.py

from core.technical.technical_runner import TechnicalAI as CoreTechnical


class TechnicalAI:

    def __init__(self):

        self.core = CoreTechnical()

    def run(self, df):

        try:

            result = self.core.run(df)

            if isinstance(result, dict):

                return float(
                    result.get("score", 0)
                )

            return float(result)

        except Exception as e:

            print(
                "TECH AI ERROR:",
                e
            )

            return 0.0