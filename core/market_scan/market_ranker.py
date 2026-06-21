# core/market_scan/market_ranker.py

class MarketRanker:

    def score(
        self,
        df,
        regime
    ):

        try:

            close = df["Close"]

            current = float(
                close.iloc[-1]
            )

            score = 50

            # =====================
            # REGIME
            # =====================
            regime_name = regime.get(
                "regime",
                "SIDE"
            )

            if regime_name == "BULL":

                score += 15

            elif regime_name == "BEAR":

                score -= 10

            elif regime_name == "CRASH":

                score -= 20

            # =====================
            # MA
            # =====================
            ma25 = (
                close
                .rolling(25)
                .mean()
                .iloc[-1]
            )

            ma50 = (
                close
                .rolling(50)
                .mean()
                .iloc[-1]
            )

            if current > ma25:

                score += 10

            if ma25 > ma50:

                score += 10

            # =====================
            # MA SLOPE
            # =====================
            ma25_prev = (
                close
                .rolling(25)
                .mean()
                .iloc[-6]
            )

            if ma25 > ma25_prev:

                score += 8

            # =====================
            # MOMENTUM
            # =====================
            momentum = (

                current

                -

                close.iloc[-20]

            ) / close.iloc[-20]

            if momentum > 0.20:

                score += 15

            elif momentum > 0.10:

                score += 8

            elif momentum < -0.10:

                score -= 10

            # =====================
            # BREAKOUT
            # =====================
            high50 = (

                close
                .rolling(50)
                .max()
                .iloc[-2]
            )

            if current > high50:

                score += 10

            # =====================
            # VOLUME
            # =====================
            if "Volume" in df.columns:

                vol_now = (
                    df["Volume"]
                    .iloc[-1]
                )

                vol_avg = (
                    df["Volume"]
                    .rolling(20)
                    .mean()
                    .iloc[-1]
                )

                if vol_avg > 0:

                    ratio = (
                        vol_now / vol_avg
                    )

                    if ratio > 2:

                        score += 10

                    elif ratio > 1.5:

                        score += 5

            return max(
                min(score, 100),
                0
            )

        except:

            return 50