class CapitalManager:

    def __init__(self):

        self.base_max = 18
        self.dd = 0.0

    def update_dd(self, dd):

        self.dd = dd

    def cash_ratio(self, regime, volatility):

        if regime == "CRASH":
            return 0.5

        if volatility > 0.05:
            return 0.3

        return 0.1

    def max_positions(self, regime, confidence):

        max_pos = self.base_max

        # DD制御
        if self.dd < -0.30:
            max_pos -= 15

        elif self.dd < -0.20:
            max_pos -= 10

        elif self.dd < -0.10:
            max_pos -= 5

        elif self.dd > -0.05 and regime == "BULL":
            max_pos += 2

        return max(6, min(max_pos, 40))