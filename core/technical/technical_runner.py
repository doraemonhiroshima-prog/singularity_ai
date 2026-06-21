     #core/technical/technical_runner.py

from core.technical.indicators import Indicators
from core.technical.breakout_detector import BreakoutDetector
from core.technical.signals import volume_score, breakout_score


class TechnicalAI:

    def __init__(self):

        self.indicators = Indicators()
        self.breakout = BreakoutDetector()

        self.memory = {
            "breakout_weight": 1.0,
            "volume_weight": 1.0,
            "trend_weight": 1.0
        }

    # =========================
    # VWAP（統合）
    # =========================
    def vwap(self, df):

        if len(df) < 20:
            return 0

        tp = (df["High"] + df["Low"] + df["Close"]) / 3
        vol = df["Volume"]

        vwap = (tp * vol).cumsum() / vol.cumsum()

        return float(vwap.iloc[-1])

    # =========================
    # LEARNING
    # =========================
    def learn(self, breakout_hit, volume_hit, trend_hit):

        lr = 0.02

        if breakout_hit:
            self.memory["breakout_weight"] += lr
        else:
            self.memory["breakout_weight"] -= lr

        if volume_hit:
            self.memory["volume_weight"] += lr
        else:
            self.memory["volume_weight"] -= lr

        if trend_hit:
            self.memory["trend_weight"] += lr
        else:
            self.memory["trend_weight"] -= lr

        for k in self.memory:
            self.memory[k] = max(min(self.memory[k], 2.5), 0.3)

    # =========================
    # MAIN
    # =========================
    def run(self, df):

        try:

            if len(df) < 60:
                return {"score": 10}

            # INDICATORS
            indicator_score = self.indicators.calculate(df)

            # VOLUME
            volume = volume_score(df)

            # BREAKOUT
            breakout = breakout_score(df)
            breakout_detect = self.breakout.detect(df)

            # TREND
            close = df["Close"]

            ma5 = close.rolling(5).mean().iloc[-1]
            ma20 = close.rolling(20).mean().iloc[-1]

            trend = 60 if ma5 > ma20 else 20

            # =========================
            # VWAP
            # =========================
            vwap_val = self.vwap(df)
            price = close.iloc[-1]

            vwap_score = 60 if price > vwap_val else 20

            # =========================
            # TOTAL SCORE
            # =========================
            total = (
                indicator_score * 0.25 +
                volume * 0.15 * self.memory["volume_weight"] +
                breakout * 0.25 * self.memory["breakout_weight"] +
                breakout_detect * 0.30 * self.memory["breakout_weight"] +
                trend * 0.15 * self.memory["trend_weight"] +
                vwap_score * 0.20
            )

            # BOOST
            if breakout_detect >= 80:
                total += 20

            if volume >= 30:
                total += 10

            momentum = (price - close.iloc[-5]) / close.iloc[-5]

            if momentum > 0.05:
                total += 10

            total = max(min(total, 100), 5)

            return {
                "score": round(total, 2),
                "indicator": round(indicator_score, 2),
                "volume": round(volume, 2),
                "breakout": round(breakout, 2),
                "trend": round(trend, 2),
                "vwap": round(vwap_val, 2),
                "memory": self.memory.copy()
            }

        except Exception as e:
            print("TECH ERROR:", e)
            return {"score": 10}