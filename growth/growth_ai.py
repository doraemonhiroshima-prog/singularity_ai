import yfinance as yf
import time


class GrowthAI:

    def analyze(self, code):

        try:
            time.sleep(0.2)

            ticker = yf.Ticker(code)
            info = ticker.info

            score = 0

            # =========================
            # EPS成長（最重要）
            # =========================
            eps_growth = info.get("earningsQuarterlyGrowth", None)

            if eps_growth is not None:

                if eps_growth > 0.3:
                    score += 80

                elif eps_growth > 0.15:
                    score += 50

                elif eps_growth > 0:
                    score += 20

                else:
                    score -= 50

            # =========================
            # 売上成長
            # =========================
            rev_growth = info.get("revenueGrowth", None)

            if rev_growth is not None:

                if rev_growth > 0.3:
                    score += 60

                elif rev_growth > 0.15:
                    score += 40

                elif rev_growth > 0:
                    score += 20

                else:
                    score -= 30

            return score

        except Exception as e:
            print("Growth ERROR:", code, e)
            return 0
