from ai.institution.flow_detector import FlowDetector
from ai.institution.order_estimator import OrderEstimator
from ai.institution.pressure_analyzer import PressureAnalyzer

class InstitutionAI:

    def __init__(self):
        self.flow = FlowDetector()
        self.order = OrderEstimator()
        self.pressure = PressureAnalyzer()

    def analyze(self, df):

        try:
            flow_score = self.flow.analyze(df)
            order_score = self.order.analyze(df)
            pressure_score = self.pressure.analyze(df)

            # =========================
            # 統合
            # =========================
            total = (
                flow_score * 0.5 +
                order_score * 0.3 +
                pressure_score * 0.2
            )

            return total

        except Exception as e:
            print("Institution ERROR:", e)
            return 0
