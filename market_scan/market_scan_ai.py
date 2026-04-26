import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


class MarketScanAI:

    def __init__(self):
        self.max_workers = 2

        # 時価総額（2〜4倍ゾーン）
        self.MIN_CAP = 5e9
        self.MAX_CAP = 5e11

    def fetch_one(self, row):

        try:
            code = row["code"]
            name = row.get("name", "")

            time.sleep(0.2)

            # 時価総額取得
            ticker = yf.Ticker(code)
            info = ticker.info
            market_cap = info.get("marketCap", None)

            if market_cap is None:
                return None

            if not (self.MIN_CAP <= market_cap <= self.MAX_CAP):
                return None

            # 株価取得
            df = yf.download(code, period="6mo", progress=False, threads=False)

            if df is None or df.empty or len(df) < 60:
                print("NG:", code)
                return None

            close = df["Close"]

            close_now = float(close.iloc[-1])
            ma25 = float(close.rolling(25).mean().iloc[-1])
            ma75 = float(close.rolling(75).mean().iloc[-1])

            ret20 = float(close.pct_change(20).iloc[-1])

            score = 0

            # トレンド
            if close_now > ma25:
                score += 30

            if close_now > ma75:
                score += 40

            # トレンド強度
            gap = (close_now - ma25) / ma25

            if gap > 0.1:
                score += 40
            elif gap > 0.05:
                score += 20

            # 中期成長
            if 0.05 < ret20 < 0.3:
                score += 40

            return {
                "code": code,
                "name": name,
                "df": df,
                "market_score": score,
                "market_cap": market_cap
            }

        except Exception as e:
            print("ERROR:", row.get("code"), e)
            return None

    def process(self):

        df_list = pd.read_csv("stock_list.csv")
        rows = df_list.to_dict("records")

        print("codes count:", len(rows))

        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.fetch_one, r) for r in rows]

            for future in as_completed(futures):
                r = future.result()
                if r:
                    results.append(r)

        print("通過銘柄:", len(results))
        return results
