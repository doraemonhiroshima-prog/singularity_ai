     # core/growth/monitor.py

import pandas as pd
import os
from datetime import datetime


class Monitor:

    def save_learning_data(self, results):

        if not results:
            return

        os.makedirs("learning_data", exist_ok=True)

        file = (
            f"learning_data/"
            f"learning_{datetime.now().strftime('%Y_%m')}.csv"
        )

        df = pd.DataFrame(results)

        try:

            old = pd.read_csv(file)

            df = pd.concat([old, df])

        except:
            pass

        df.to_csv(file, index=False)

        print("✅ learning saved")