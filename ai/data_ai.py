import glob
import os
import pandas as pd

from core.data_pipeline.data_cleaner import clean_df


class DataAI:

    def load(self):

        files = glob.glob("data/*.csv")

        print("FILES:", len(files))

        data_map = {}

        for f in files:

            try:

                name = os.path.basename(f)

                if (
                    "stock_list" in name or
                    "training_data" in name
                ):
                    continue

                code = name.replace(".csv", "")

                df = pd.read_csv(f)

                df = clean_df(df)

                if len(df) < 100:
                    continue

                data_map[code] = df.reset_index(drop=True)

            except Exception as e:

                print("LOAD ERROR:", f, e)

        print("DATA:", len(data_map))

        return data_map