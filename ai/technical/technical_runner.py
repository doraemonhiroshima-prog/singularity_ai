class TechnicalRunner:

    def analyze(self, df):

        try:
            close = df["Close"]
            volume = df["Volume"]

            score = 0

            # =========================
            # トレンド
            # =========================
            ma5 = close.rolling(5).mean().iloc[-1]
            ma20 = close.rolling(20).mean().iloc[-1]

            if ma5 > ma20:
                score += 30

            if close.iloc[-1] > ma5:
                score += 20

            # =========================
            # モメンタム
            # =========================
            change = close.pct_change().iloc[-1]

            if change > 0.02:
                score += 30
            elif change > 0:
                score += 10

            # =========================
            # 出来高（機関の匂い）
            # =========================
            vol_now = volume.iloc[-1]
            vol_avg = volume.rolling(20).mean().iloc[-1]

            if vol_avg > 0:
                ratio = vol_now / vol_avg

                if ratio > 2:
                    score += 40
                elif ratio > 1.5:
                    score += 20

            # =========================
            # ボラ（勢い）
            # =========================
            vol = close.pct_change().rolling(10).std().iloc[-1]

            if vol > 0.03:
                score += 20

            return score

        except:
            return 0
