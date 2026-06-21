# core/news/relevance_filter.py

class RelevanceFilter:

    def __init__(self):

        self.related_words = [

            # 業績
            "上方修正",
            "下方修正",
            "増益",
            "減益",
            "黒字",
            "赤字",
            "業績",

            # 株主還元
            "自社株買い",
            "増配",
            "減配",
            "配当",

            # 成長
            "受注",
            "契約",
            "提携",
            "新製品",
            "新サービス",

            # テーマ
            "AI",
            "生成AI",
            "LLM",
            "DX",
            "SaaS",

            "EV",
            "半導体",
            "GPU",
            "NVIDIA",

            # M&A
            "TOB",
            "買収",
            "資本業務提携",

            # その他
            "決算",
            "中期計画",
            "設備投資",
            "工場"
        ]

    # =========================
    # 関連度スコア
    # =========================
    def score(
        self,
        text,
        keyword
    ):

        score = 0

        text = str(text)

        # 会社名
        if keyword:

            if keyword in text:
                score += 5

        # 関連ワード
        for word in self.related_words:

            if word in text:
                score += 1

        return score

    # =========================
    # フィルタ
    # =========================
    def filter_texts(
        self,
        texts,
        keyword
    ):

        result = []

        for text in texts:

            s = self.score(
                text,
                keyword
            )

            # 関連度2以上のみ採用
            if s >= 2:

                result.append(text)

        return result