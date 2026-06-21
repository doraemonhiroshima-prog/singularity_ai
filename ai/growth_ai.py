# ai/growth_ai.py

import json
import random

from core.growth.evaluator import Evaluator
from core.growth.adaptive_learning import AdaptiveLearning
from core.growth.performance_memory import PerformanceMemory
from core.growth.monitor import Monitor
from core.growth.fix_names import FixNames


class GrowthAI:

    def __init__(self, path="config.json"):

        self.path = path

        self.evaluator = Evaluator()

        self.learning = AdaptiveLearning()

        self.memory = PerformanceMemory()

        self.monitor = Monitor()

        self.fix_names = FixNames()

    # =====================================================
    # RUN
    # =====================================================
    def run(

        self,
        results,

        use_learning=True,

        use_monitor=True,

        use_fix_names=False
    ):

        # =================================================
        # EVALUATION
        # =================================================
        metrics = (
            self.evaluator
            .evaluate(results)
        )

        # =================================================
        # CONFIG LOAD
        # =================================================
        try:

            with open(
                self.path,
                "r"
            ) as f:

                config = json.load(f)

        except:

            config = {

                "score_threshold": 60,

                "take_profit": 0.15,

                "stop_loss": 0.05
            }

        # =================================================
        # LEARNING
        # =================================================
        if use_learning:

            acc5 = metrics["acc5"]

            if acc5 < 0.5:

                config["score_threshold"] += (
                    random.randint(-2, 2)
                )

            else:

                config["take_profit"] += (
                    random.uniform(
                        -0.01,
                        0.01
                    )
                )

        # =================================================
        # SAVE CONFIG
        # =================================================
        with open(
            self.path,
            "w"
        ) as f:

            json.dump(
                config,
                f,
                indent=2
            )

        # =================================================
        # MONITOR
        # =================================================
        if use_monitor:

            self.monitor.save_learning_data(
                results
            )

        # =================================================
        # MEMORY
        # =================================================
        for r in results:

            try:

                self.memory.add(

                    code=r.get(
                        "code",
                        "UNKNOWN"
                    ),

                    factors=r.get(
                        "factors",
                        {}
                    ),

                    profit=r.get(
                        "profit",
                        0
                    ),

                    regime=r.get(
                        "regime",
                        "UNKNOWN"
                    )
                )

            except:

                continue

        # =================================================
        # ADAPTIVE LEARNING
        # =================================================
        if use_learning:

            for r in results:

                try:

                    self.learning.update(

                        factors=r.get(
                            "factors",
                            {}
                        ),

                        profit=r.get(
                            "profit",
                            0
                        )
                    )

                except:

                    continue

        # =================================================
        # FIX SYSTEM
        # =================================================
        if use_fix_names:

            self.fix_names.run(

                fix_code=True,

                repair_names=True,

                update_stock_list=True
            )

        # =================================================
        # RETURN
        # =================================================
        return {

            "metrics": metrics,

            "config": config,

            "weights": (
                self.learning.weights()
            ),

            "memory_winrate": (
                self.memory.winrate()
            ),

            "memory_profit": (
                self.memory.avg_profit()
            ),

            "regime_stats": (
                self.memory.regime_stats()
            )
        }