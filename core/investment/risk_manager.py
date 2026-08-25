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
        holdings,
        cash,
        current_dd,
        signal
    ):

        try:

            # =========================
            # POSITION LIMIT
            # =========================
            if len(holdings) >= self.max_positions:
                return False

            # =========================
            # CASH
            # =========================
            if cash <= 0:
                return False

            # =========================
            # SIGNAL
            # =========================
            if signal.get("signal") != "BUY":
                return False

            # =========================
            # DD FILTER
            # =========================
            if current_dd >= self.max_drawdown:
                return False

            return True

        except Exception:

            return False

    # =====================================================
    # POSITION SIZE
    # =====================================================
    def position_size(
        self,
        cash,
        price,
        current_dd=0,
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
            # VOLATILITY
            # =========================
            if volatility > 0.08:
                risk *= 0.5

            # =========================
            # DD
            # =========================
            if current_dd > 0.15:
                risk *= 0.5

            # =========================
            # CASH
            # =========================
            risk_cash = cash * risk

            qty = int(risk_cash / price)

            return max(qty, 1)

        except Exception:

            return 1