# core/data_pipeline/run_collection.py

from core.data_pipeline.history_collector import HistoryCollector
from core.data_pipeline.data_cleaner import clean_df


class RunCollection:

    def __init__(self):

        self.market_data = {}

        self.collector = HistoryCollector()

    def load_market_data(self, codes):

        cleaned = {}

        for code in codes:

            try:

                # =========================
                # FETCH
                # =========================
                df = self.collector.fetch(code)

                if df is None:
                    continue

                # =========================
                # CLEAN
                # =========================
                df = clean_df(df)

                if df is None:
                    continue

                if len(df) < 100:
                    continue

                cleaned[code] = (
                    df.reset_index(drop=True)
                )

            except Exception as e:

                print(
                    f"[DATA ERROR] {code}: {e}"
                )

        self.market_data = cleaned

        return cleaned

    def build_ai_input(self):

        return {
            "market_data": self.market_data,
            "symbols": list(
                self.market_data.keys()
            ),
            "total_symbols": len(
                self.market_data
            )
        }