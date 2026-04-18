import pandas as pd
import yfinance as yf
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed


class TechnicalAI:

    def __init__(self):
        self.cache = {}

    def get_data(self, code):

        if code in self.cache:
            return self.cache[code]

        for _ in range(2):
            try:
                df = yf.download(
                    code,
                    period="3mo",
                    progress=False,
                    threads=False
                )
                if df is not None and not df.empty:
                    self.cache[code] = df
                    return df
            except:
                pass

            time.sleep(1)

        return None

    def calc_score(self, df):

        score = 0
        close = df["Close"]
        vol = df["Volume"]

        try:
            ma5 = close.rolling(5).mean()
            ma25 = close.rolling(25).mean()

            if ma5.iloc[-1] > ma25.iloc[-1]:
                score += 20

            if close.iloc[-1] > close.iloc[-5]:
                score += 20

            if close.iloc[-1] >= close.max():
                score += 30

            if vol.iloc[-1] > vol.rolling(10).mean().iloc[-1]:
                score += 30

        except:
            pass

        return score

    # 並列1タスク
    def worker(self, s):
        code = s["code"]

        df = self.get_data(code)
        if df is None:
            return None

        score = self.calc_score(df)
        s["T"] = score

        print(f"{code} → {score}")
        return s

    def process(self, stocks):

        results = []

        CHUNK = 100  # 分割
        MAX_WORKERS = 5  # 並列数（多すぎるとBAN）

        for start in range(0, len(stocks), CHUNK):

            batch = stocks[start:start+CHUNK]
            print(f"\n=== BATCH {start} → {start+len(batch)} ===")

            with ThreadPoolExecutor(max_workers=MAX_WORKERS) as exe:
                futures = [exe.submit(self.worker, s) for s in batch]

                for f in as_completed(futures):
                    r = f.result()
                    if r:
                        results.append(r)

            # バッチ休憩（重要）
            time.sleep(10 + random.uniform(0, 5))

        return results
