class StockContext:

    def __init__(self):
        pass

    def get_context_score(self, name):

        score = 0

        # 成長系
        if any(k in name for k in ["AI", "半導体", "EV"]):
            score += 0.5

        # ディフェンシブ
        if any(k in name for k in ["電力", "通信", "銀行"]):
            score += 0.2

        # リスク
        if any(k in name for k in ["不動産", "中国"]):
            score -= 0.3

        return max(min(score, 1), -1)