# ai/investment_ai.py

from core.investment.executor import Executor
from core.investment.risk_manager import RiskManager
from core.investment.capital_allocator import CapitalAllocator

from core.investment.sell_ai import sell_signal

from core.investment import config


class InvestmentAI:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(
        self,
        portfolio
    ):

        self.portfolio = portfolio

        self.executor = Executor(
            portfolio
        )

        self.risk_manager = RiskManager()

        self.capital_allocator = (
            CapitalAllocator()
        )

        # =========================
        # CONFIG
        # =========================
        self.config = config

    # =====================================================
    # FINAL DECISION
    # =====================================================
    def decide(
        self,
        signal,
        portfolio
    ):

        try:

            # =========================
            # SIGNAL
            # =========================
            if signal.get(
                "signal"
            ) != "BUY":

                return False

            # =========================
            # CONFIDENCE
            # =========================
            confidence = float(
                signal.get(
                    "confidence",
                    0
                )
            )

            if confidence < self.config.MIN_SCORE:

                return False

            # =========================
            # RISK
            # =========================
            ok = self.risk_manager.check(
                portfolio,
                signal
            )

            if not ok:

                return False

            return True

        except:

            return False

    # =====================================================
    # SELL CHECK
    # =====================================================
    def sell_check(
        self,
        df,
        buy_price,
        peak_price=None
    ):

        return sell_signal(
            df=df,
            buy_price=buy_price,
            peak_price=peak_price
        )

    # =====================================================
    # POSITION SIZE
    # =====================================================
    def position_size(
        self,
        price,
        confidence=50,
        volatility=0.03
    ):

        return self.risk_manager.position_size(
            portfolio=self.portfolio,
            price=price,
            confidence=confidence,
            volatility=volatility
        )

    # =====================================================
    # CAPITAL ALLOCATE
    # =====================================================
    def allocate(
        self,
        cash,
        signals
    ):

        return self.capital_allocator.allocate(
            cash,
            signals
        )

    # =====================================================
    # EXECUTE
    # =====================================================
    def execute(
        self,
        decisions,
        data_map
    ):

        return self.executor.execute(
            decisions,
            data_map
        )

    # =====================================================
    # RISK CHECK
    # =====================================================
    def check_risk(
        self,
        signal
    ):

        return self.risk_manager.check(
            self.portfolio,
            signal
        )