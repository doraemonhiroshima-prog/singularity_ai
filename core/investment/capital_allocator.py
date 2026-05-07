class CapitalAllocator:

    def allocate(self, cash, signals):

        result = []

        if len(signals) == 0:
            return result

        size = cash / len(signals)

        for s in signals:

            s["capital"] = size

            result.append(s)

        return result