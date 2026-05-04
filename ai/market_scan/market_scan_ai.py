import yfinance as yf

class MarketScanAI:

    def fetch_one(self, stock):

        code = stock["code"]

        try:
            df = yf.download(code, period="1y", progress=False)


            if df is None or df.empty:
                print(f"NG: {code}")
                return None

            return {
                "code": code,
                "name": stock["name"],
                "df": df,
                "market_score": 50
            }

        except Exception as e:
            print(f"Market ERROR: {code} {e}")
            return None
