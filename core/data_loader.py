import os
import glob
import pandas as pd

from core.data_pipeline.data_cleaner import clean_df


def load_all(start_year=None, end_year=None):

    files = glob.glob("data/*.csv")

    data_map = {}

    for f in files:

        if "stock_list" in f:
            continue

        try:
            code = os.path.basename(f).replace(".csv", "")
            df = pd.read_csv(f)

            df = clean_df(df)

            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

                if start_year:
                    df = df[df["Date"].dt.year >= start_year]

                if end_year:
                    df = df[df["Date"].dt.year <= end_year]

            if len(df) < 120:
                continue

            data_map[code] = df.reset_index(drop=True)

        except:
            continue

    return data_map