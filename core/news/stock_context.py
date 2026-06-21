   # core/news/stock_context.py

class StockContext:

    def __init__(self):

        self.theme_bonus = {

            "AI": 0.40,
            "半導体": 0.35,
            "EV": 0.30,
            "DX": 0.25,
            "バイオ": 0.20,
            "ロボット": 0.20
        }

    # =========================
    # CONTEXT SCORE
    # =========================
    def get_context_score(
        self,
        name,
        themes=None
    ):

        score = 0

        # =========================
        # COMPANY NAME
        # =========================
        if any(
            k in name
            for k in [
                "AI",
                "人工知能",
                "EV"
            ]
        ):
            score += 0.5

        if any(
            k in name
            for k in [
                "半導体",
                "データ"
            ]
        ):
            score += 0.3

        if any(
            k in name
            for k in [
                "銀行",
                "保険"
            ]
        ):
            score -= 0.2

        # =========================
        # THEME BONUS
        # =========================
        if themes:

            for theme, theme_score in themes:

                score += self.theme_bonus.get(
                    theme,
                    0
                )

                score += (
                    theme_score / 100
                ) * 0.2

        return max(
            min(score, 1),
            -1
        )