# ai/institution_ai.py

from core.institution.institution_core import (
    InstitutionCore
)


class InstitutionAI:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(

        self,

        mode="live",

        use_learning=True,

        save_weights=False
    ):

        self.core = InstitutionCore(

            mode=mode,

            use_learning=
                use_learning,

            save_weights=
                save_weights
        )

    # =====================================================
    # RUN
    # =====================================================
    def run(self, df):

        return self.core.analyze(df)