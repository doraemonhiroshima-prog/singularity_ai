# ai/data_ai.py

import pandas as pd

from core.data_pipeline.run_collection import RunCollection


class DataAI:

    def __init__(self):

        self.runner = RunCollection()

    def run(self, codes):

        market_data = (
            self.runner.load_market_data(
                codes
            )
        )

        stock_info = {}

        try:

            df = pd.read_csv(
                "data/stock_list.csv"
            )

            for _, row in df.iterrows():

                code = str(
                    row["code"]
                )

                name = str(
                    row["name"]
                )

                stock_info[code] = name

        except Exception as e:

            print(
                "STOCK INFO ERROR:",
                e
            )

        return {

            "status": "success",

            "market_data": market_data,

            "stock_info": stock_info
        }