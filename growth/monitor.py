import time
import pandas as pd
import yfinance as yf
import os
from datetime import datetime

from ai.market_scan.pipeline_controller import PipelineController
from news.news_ai import NewsAI
from ai.Future_prediction.predict_ai import PredictAI


# =========================
# 設定
# =========================
USE_OFFLINE = True  # ← ★ここ切り替え
SAVE_CSV = True
INTERVAL_SEC = 10   # API叩く間隔


# =========================
# 市場時間チェック（日本）
# =========================
def is_market_open():
    now = datetime.now()

    if now.weekday() >= 5:
        return False

    hour = now.hour
    minute = now.minute

    if (9 <= hour < 11) or (hour == 11 and minute <= 30):
        return True

    if (12 <= hour < 15):
        return True

    return False


# =========================
# オフラインデータ取得
# =========================
def load_offline_data(code):
    try:
        file = f"offline_data/{code}.csv"
        if os.path.exists(file):
            df = pd.read_csv(file)
            return df
    except:
        pass
    return None


# =========================
# データ取得（安全版）
# =========================
def safe_download(code):

    # ★ オフライン優先
    if USE_OFFLINE:
        df = load_offline_data(code)
        if df is not None:
            return df

    # ★ API（低頻度）
    try:
        df = yf.download(
            code,
            period="5d",
            interval="15m",
            progress=False,
            threads=False
        )

        time.sleep(5)  # ★ 超重要（制限回避）

        if df is None or df.empty:
            return None

        return df

    except Exception as e:
        print("DL ERROR:", code, e)
        return None


# =========================
# メインAI
# =========================
class MonitorAI:

    def __init__(self):
        self.news_ai = NewsAI()
        self.predict_ai = PredictAI()

    def run(self):

        print("=== SMART MONITOR START ===")

        pipeline = PipelineController()
        stocks = pipeline.run()

        watch_list = [r["code"] for r in stocks[:10]]
        print("WATCH:", watch_list)

        while True:

            # ★ オフラインなら常時実行
            if USE_OFFLINE or is_market_open():

                results = []

                for code in watch_list:

                    try:
                        df = safe_download(code)

                        if df is None or df.empty:
                            continue

                        price = float(df["Close"].iloc[-1])
                        volume = float(df["Volume"].iloc[-1])
                        change = float(df["Close"].pct_change().iloc[-1])

                        news = self.news_ai.analyze(code, code)

                        # AI予測
                        try:
                            prob = self.predict_ai.predict(
                                price,
                                volume,
                                change,
                                news["score"]
                            )
                        except:
                            prob = 0.5

                        results.append({
                            "Time": pd.Timestamp.now(),
                            "Code": code,
                            "Price": price,
                            "Volume": volume,
                            "Change": change,
                            "News": news["score"],
                            "AI_Prob": prob
                        })

                        print(f"{code} | {price:.2f} | AI:{prob:.2f}")

                    except Exception as e:
                        print("ERROR:", code, e)

                # =========================
                # 保存
                # =========================
                if SAVE_CSV and len(results) > 0:

                    df_save = pd.DataFrame(results)

                    os.makedirs("learning_data", exist_ok=True)

                    file = f"learning_data/learning_{datetime.now().strftime('%Y_%m')}.csv"

                    try:
                        old = pd.read_csv(file)
                        df_save = pd.concat([old, df_save])
                    except:
                        pass

                    df_save.to_csv(file, index=False)

                print("---- CYCLE ----")

                time.sleep(INTERVAL_SEC)

            else:
                print("市場外 → 休止")
                time.sleep(60)


# =========================
# 実行
# =========================
if __name__ == "__main__":
    MonitorAI().run()
