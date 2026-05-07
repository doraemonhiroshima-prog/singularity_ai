import pandas as pd
import time
import os

from core.data_pipeline.history_collector import HistoryCollector


CSV_PATH = "data/stock_list.csv"

SLEEP = 1
BATCH_SIZE = 50
BATCH_SLEEP = 10


def run():

    print("=== データ取得開始 ===")

    df_list = pd.read_csv(CSV_PATH)
    df_list = df_list.drop_duplicates(subset=["code"])

    collector = HistoryCollector()

    for i, row in df_list.iterrows():

        code = row["code"]

        try:
            path = f"data/{code}.csv"

            print(f"DL: {code}")

            df = collector.fetch(code)

            if df is None or len(df) < 200:
                print(f"SKIP: {code}")
                continue

            df.to_csv(path, index=False)

            time.sleep(SLEEP)

        except Exception as e:
            print(f"ERROR: {code} {e}")

        if (i + 1) % BATCH_SIZE == 0:
            print("=== 休憩 ===")
            time.sleep(BATCH_SLEEP)

    print("=== 完了 ===")


if __name__ == "__main__":
    run()
