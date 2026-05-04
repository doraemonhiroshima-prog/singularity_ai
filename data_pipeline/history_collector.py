import yfinance as yf
import pandas as pd


class HistoryCollector:

    def fetch(self, code):

        try:
            ticker = yf.Ticker(code)

            df = ticker.history(
                start="2005-01-01",
                end=None,
                auto_adjust=True
            )

            if df is None or len(df) == 0:
                return None

            df = df.reset_index()

            # カラム統一
            df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

            # 日付を文字列に
            df["Date"] = df["Date"].astype(str)

            return df

        except Exception as e:
            print("FETCH ERROR:", code, e)
            return None
