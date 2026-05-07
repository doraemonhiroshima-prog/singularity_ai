# ai/data_ai.py

import glob
import os
import pandas as pd

from core.data_pipeline.data_cleaner import clean_df


class DataAI:

    def __init__(self):
        pass

    def load_all(self):

        files = glob.glob("data/*.csv")

        print("FILES:", len(files))

        data_map = {}

        for f in files:

            try:
                name = os.path.basename(f)

                if "stock_list" in name:
                    continue

                df = pd.read_csv(f)

                df = clean_df(df)

                if len(df) < 100:
                    continue

                code = name.replace(".csv", "")

                data_map[code] = df.reset_index(drop=True)

            except Exception as e:
                print("LOAD ERROR:", f, e)

        print("DATA:", len(data_map))

        return data_map