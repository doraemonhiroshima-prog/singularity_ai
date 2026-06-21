# core/investment/risk_manager.py

class RiskManager:

    def __init__(self):

        self.base_risk = 0.03

        self.max_positions = 5

        self.max_drawdown = 0.25

    # =====================================================
    # CHECK
    # =====================================================
    def check(
        self,
        portfolio,
        signal
    ):

        try:

            # =========================
            # POSITION LIMIT
            # =========================
            if len(
                portfolio.positions
            ) >= self.max_positions:

                return False

            # =========================
            # CASH
            # =========================
            if portfolio.cash <= 0:

                return False

            # =========================
            # SIGNAL
            # =========================
            if signal.get(
                "signal"
            ) != "BUY":

                return False

            # =========================
            # DD FILTER
            # =========================
            current_dd = getattr(
                portfolio,
                "drawdown",
                0
            )

            if current_dd >= self.max_drawdown:

                return False

            return True

        except:

            return False

    # =====================================================
    # POSITION SIZE
    # =====================================================
    def position_size(
        self,
        portfolio,
        price,
        confidence=50,
        volatility=0.03
    ):

        try:

            # =========================
            # CONFIDENCE
            # =========================
            if confidence >= 85:

                risk = 0.07

            elif confidence >= 70:

                risk = 0.05

            elif confidence >= 60:

                risk = 0.04

            else:

                risk = 0.02

            # =========================
            # VOLATILITY REDUCE
            # =========================
            if volatility > 0.08:

                risk *= 0.5

            # =========================
            # DD REDUCE
            # =========================
            dd = getattr(
                portfolio,
                "drawdown",
                0
            )

            if dd > 0.15:

                risk *= 0.5

            # =========================
            # CASH
            # =========================
            risk_cash = (
                portfolio.cash *
                risk
            )

            qty = int(
                risk_cash / price
            )

            return max(qty, 1)

        except:

            return 1