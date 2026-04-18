import time
import pandas as pd
import yfinance as yf
from datetime import datetime

from market_scan.pipeline_controller import PipelineController
from news.news_ai import NewsAI
from Future_prediction.predict_ai import PredictAI


# =========================
# 市場時間チェック（日本）
# =========================
def is_market_open():
    now = datetime.now()

    # 土日除外
    if now.weekday() >= 5:
        return False

    hour = now.hour
    minute = now.minute

    # 9:00〜11:30
    if (9 <= hour < 11) or (hour == 11 and minute <= 30):
        return True

    # 12:30〜15:00
    if (12 <= hour < 15):
        return True

    return False


class MonitorAI:

    def __init__(self):
        self.news_ai = NewsAI()
        self.predict_ai = PredictAI()

    def run(self):

        print("=== SMART MONITOR START ===")

        # =========================
        # 銘柄取得
        # =========================
        pipeline = PipelineController()
        stocks = pipeline.run()

        watch_list = [r["code"] for r in stocks[:10]]
        print("WATCH:", watch_list)

        # =========================
        # 監視ループ
        # =========================
        while True:

            if is_market_open():

                results = []

                for code in watch_list:

                    try:
                        df = yf.download(code, period="1d", interval="1m", progress=False)

                        if df is None or df.empty:
                            continue

                        price = float(df["Close"].iloc[-1].item())
                        volume = float(df["Volume"].iloc[-1].item())
                        change = float(df["Close"].pct_change().iloc[-1].item())

                        news = self.news_ai.analyze(code, code)

                        # ★ AI予測
                        try:
                            prob = self.predict_ai.predict(
                                price,
                                volume,
                                change,
                                news["score"]
                            )
                        except:
                            prob = 0

                        results.append({
                            "Time": pd.Timestamp.now(),
                            "Code": code,
                            "Price": price,
                            "Volume": volume,
                            "Change": change,
                            "News": news["score"]
                        })

                        print(f"{code} | {price:.2f} | AI:{prob:.2f}")

                        time.sleep(2)

                    except Exception as e:
                        print("ERROR:", code, e)

                # =========================
                # 保存（月ごと）
                # =========================
                if len(results) > 0:

                    df_save = pd.DataFrame(results)

                    file = f"learning_{datetime.now().strftime('%Y_%m')}.csv"

                    try:
                        old = pd.read_csv(file)
                        df_save = pd.concat([old, df_save])
                    except:
                        pass

                    df_save.to_csv(file, index=False)

                print("---- MARKET CYCLE ----")

                time.sleep(60)

            else:
                print("市場外 → 休止")
                time.sleep(600)


if __name__ == "__main__":
    MonitorAI().run()
