import yfinance as yf
import pandas as pd
import time
import os


class HistoryCollector:

    def __init__(self):
        os.makedirs("offline_data", exist_ok=True)

    def fetch(self, code, period="5y"):

        try:
            print("DL:", code)

            df = yf.download(
                code,
                period=period,
                interval="1d",
                progress=False,
                threads=False
            )

            if df is None or df.empty:
                print("NG:", code)
                return None

            df.to_csv(f"offline_data/{code}.csv")

            time.sleep(3)

            return df

        except Exception as e:
            print("ERROR:", code, e)
            return None

    def fetch_all(self, codes):

        results = {}

        for code in codes:
            df = self.fetch(code)
            if df is not None:
                results[code] = df

        print("=== 完了 ===")
        return results
