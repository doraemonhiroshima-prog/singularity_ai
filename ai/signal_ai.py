from core.signal.signals import SignalGenerator


class SignalAI:

    def __init__(self):

        self.core = SignalGenerator()

    def run(
        self,
        data,
        weights,
        threshold
    ):

        return self.core.generate(
            data,
            weights,
            threshold
        )