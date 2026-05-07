import pandas as pd

class Indicators:

    def calculate(self, df):

        try:
            ma5 = df["Close"].rolling(5).mean().iloc[-1]
            ma20 = df["Close"].rolling(20).mean().iloc[-1]

            if ma20 == 0:
                return 50

            diff = (ma5 - ma20) / ma20

            return 50 + diff * 200

        except:
            return 50