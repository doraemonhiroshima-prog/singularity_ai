from core.technical.indicators import Indicators

class TechnicalAI:

    def __init__(self):
        self.core = Indicators()

    def run(self, df):
        return self.core.calculate(df)