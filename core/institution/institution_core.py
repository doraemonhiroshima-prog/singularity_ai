# core/institution/institution_core.py

import os
import json


from core.institution.flow_detector import (
    FlowDetector
)

from core.institution.pressure_analyzer import (
    PressureAnalyzer
)

from core.institution.order_estimator import (
    OrderEstimator
)


class InstitutionCore:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(

        self,

        mode="live",

        use_learning=True,

        save_weights=True

    ):

        self.flow_detector = (
            FlowDetector()
        )

        self.pressure_analyzer = (
            PressureAnalyzer()
        )

        self.order_estimator = (
            OrderEstimator()
        )

        # =================================================
        # MODE
        # =================================================
        self.mode = mode

        self.use_learning = (
            use_learning
        )

        self.save_weights_flag = (
            save_weights
        )

        # =================================================
        # LEARNING RATE
        # =================================================
        if mode == "backtest":

            self.learning_rate = 0.03

        else:

            self.learning_rate = 0.003

        # =================================================
        # WEIGHTS
        # =================================================
        self.flow_weight = 0.40

        self.pressure_weight = 0.35

        self.order_weight = 0.25

        # =================================================
        # FILE
        # =================================================
        self.weight_file = (
            "data/institution_weights.json"
        )

        # =================================================
        # LOAD
        # =================================================
        self.load_weights()

    # =====================================================
    # LOAD WEIGHTS
    # =====================================================
    def load_weights(self):

        try:

            if not os.path.exists(
                self.weight_file
            ):

                return

            with open(

                self.weight_file,

                "r",

                encoding="utf-8"

            ) as f:

                data = json.load(f)

            self.flow_weight = float(
                data.get(
                    "flow_weight",
                    0.40
                )
            )

            self.pressure_weight = float(
                data.get(
                    "pressure_weight",
                    0.35
                )
            )

            self.order_weight = float(
                data.get(
                    "order_weight",
                    0.25
                )
            )

            print(
                "INSTITUTION WEIGHTS LOADED"
            )

        except Exception as e:

            print(
                "LOAD WEIGHTS ERROR:",
                e
            )

    # =====================================================
    # SAVE WEIGHTS
    # =====================================================
    def save_weights(self):

        try:

            if not self.save_weights_flag:

                return

            data = {

                "flow_weight":
                    self.flow_weight,

                "pressure_weight":
                    self.pressure_weight,

                "order_weight":
                    self.order_weight
            }

            with open(

                self.weight_file,

                "w",

                encoding="utf-8"

            ) as f:

                json.dump(

                    data,

                    f,

                    indent=4
                )

        except Exception as e:

            print(
                "SAVE WEIGHTS ERROR:",
                e
            )

    # =====================================================
    # NORMALIZE
    # =====================================================
    def normalize_weights(self):

        total = (

            self.flow_weight +

            self.pressure_weight +

            self.order_weight
        )

        if total <= 0:

            self.flow_weight = 0.40

            self.pressure_weight = 0.35

            self.order_weight = 0.25

            return

        self.flow_weight /= total

        self.pressure_weight /= total

        self.order_weight /= total

    # =====================================================
    # ANALYZE
    # =====================================================
    def analyze(self, df):

        try:

            # =================================================
            # FLOW
            # =================================================
            flow = (
                self.flow_detector
                .detect(df)
            )

            # =================================================
            # PRESSURE
            # =================================================
            pressure = (
                self.pressure_analyzer
                .analyze(df)
            )

            # =================================================
            # ORDER
            # =================================================
            order = (
                self.order_estimator
                .estimate(df)
            )

            # =================================================
            # SCORES
            # =================================================
            flow_score = float(
                flow.get(
                    "score",
                    50
                )
            )

            pressure_score = float(
                pressure.get(
                    "score",
                    50
                )
            )

            order_score = float(
                order.get(
                    "score",
                    50
                )
            )

            # =================================================
            # FINAL
            # =================================================
            score = (

                flow_score *
                self.flow_weight +

                pressure_score *
                self.pressure_weight +

                order_score *
                self.order_weight
            )

            score = max(
                min(score, 100),
                0
            )

            # =================================================
            # INSTITUTION HOLD
            # =================================================
            institution_hold = False

            if (

                flow_score >= 75 and
                pressure_score >= 70

            ):

                institution_hold = True

            if (

                flow_score >= 75 and
                order_score >= 70

            ):

                institution_hold = True

            if score >= 80:

                institution_hold = True

            # =================================================
            # RETURN
            # =================================================
            return {

                "score": score,

                "institution_hold":
                    institution_hold,

                "flow_score":
                    flow_score,

                "pressure_score":
                    pressure_score,

                "order_score":
                    order_score
            }

        except Exception as e:

            print(
                "INSTITUTION ANALYZE ERROR:",
                e
            )

            return {

                "score": 50,

                "institution_hold": False
            }

    # =====================================================
    # LEARN
    # =====================================================
    def learn(

        self,

        flow_score,

        pressure_score,

        order_score,

        profit_pct
    ):

        try:

            if not self.use_learning:

                return

            # =============================================
            # GOOD TRADE
            # =============================================
            if profit_pct > 0:

                if flow_score >= 70:

                    self.flow_weight += (
                        self.learning_rate
                    )

                if pressure_score >= 70:

                    self.pressure_weight += (
                        self.learning_rate
                    )

                if order_score >= 70:

                    self.order_weight += (
                        self.learning_rate
                    )

            # =============================================
            # BAD TRADE
            # =============================================
            else:

                if flow_score >= 70:

                    self.flow_weight -= (
                        self.learning_rate
                    )

                if pressure_score >= 70:

                    self.pressure_weight -= (
                        self.learning_rate
                    )

                if order_score >= 70:

                    self.order_weight -= (
                        self.learning_rate
                    )

            # =============================================
            # MIN LIMIT
            # =============================================
            self.flow_weight = max(
                self.flow_weight,
                0.05
            )

            self.pressure_weight = max(
                self.pressure_weight,
                0.05
            )

            self.order_weight = max(
                self.order_weight,
                0.05
            )

            # =============================================
            # NORMALIZE
            # =============================================
            self.normalize_weights()

            # =============================================
            # SAVE
            # =============================================
            self.save_weights()

        except Exception as e:

            print(
                "INSTITUTION LEARN ERROR:",
                e
            )