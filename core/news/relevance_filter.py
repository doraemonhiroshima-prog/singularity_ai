class RelevanceFilter:

    def __init__(self):
        pass

    def is_relevant(self, text, keyword):

        if keyword in text:
            return True

        # 関連ワード
        related = ["株", "決算", "業績", "市場"]

        for r in related:
            if r in text:
                return True

        return False