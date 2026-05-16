# core/growth/performance_memory.py

class PerformanceMemory:

 def __init__(self):

    self.history = []

# =========================
# ADD
# =========================
def add(
    self,
    code,
    factors,
    profit,
    regime
):

    self.history.append({
        "code": code,
        "factors": factors,
        "profit": profit,
        "regime": regime
    })

    # 履歴制限
    self.history = self.history[-1000:]

# =========================
# WINRATE
# =========================
def winrate(self):

    if len(self.history) == 0:
        return 0.5

    wins = len([
        h for h in self.history
        if h["profit"] > 0
    ])

    return wins / len(self.history)

# =========================
# AVG PROFIT
# =========================
def avg_profit(self):

    if len(self.history) == 0:
        return 0

    return sum([
        h["profit"]
        for h in self.history
    ]) / len(self.history)

# =========================
# REGIME ANALYSIS
# =========================
def regime_stats(self):

    stats = {}

    for h in self.history:

        regime = h["regime"]

        if regime not in stats:

            stats[regime] = []

        stats[regime].append(
            h["profit"]
        )

    result = {}

    for regime, vals in stats.items():

        result[regime] = {

            "count": len(vals),

            "avg_profit": (
                sum(vals) / len(vals)
            )
        }

    return result

