class WinRateLearning:

    def __init__(self):

        self.wins = 0
        self.losses = 0

    def update(self, profit):

        if profit > 0:

            self.wins += 1

        else:

            self.losses += 1

    def rate(self):

        total = self.wins + self.losses

        if total == 0:
            return 0.5

        return self.wins / total