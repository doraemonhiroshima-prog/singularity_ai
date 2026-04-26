import yfinance as yf
import time


def fetch_data(codes):

    data = {}

    for code in codes:

        try:
            df = yf.download(code, period="6mo", interval="1d", progress=False)

            if df is None or df.empty:
                continue

            data[code] = df

            time.sleep(1.5)  # ★制限対策（超重要）

        except Exception as e:
            print("DL ERROR:", code, e)

    return data
