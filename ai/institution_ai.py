from core.institution.institution_core import InstitutionCore

class InstitutionAI:

    def __init__(self):
        self.core = InstitutionCore()

    def run(self, df):
        return self.core.analyze(df)