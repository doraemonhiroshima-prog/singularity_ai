# core/news/sentiment_engine.py

from .news_collector import NewsCollector
from .relevance_filter import RelevanceFilter


class SentimentEngine:

    def __init__(self):

        self.collector = NewsCollector()

        self.filter = RelevanceFilter()

        # =========================
        # 材料評価
        # =========================
        self.keywords = {

            # 超強材料
            "TOB": 5,
            "自社株買い": 4,
            "増配": 4,
            "最高益": 4,
            "上方修正": 4,
            "大口受注": 4,

            # 強材料
            "業績予想": 3,
            "通期上方修正": 3,
            "提携": 3,
            "黒字転換": 3,

            # 中材料
            "生成AI": 2,
            "新製品": 2,

            # 弱材料
            "発表": 1,

            # 悪材料
            "下方修正": -3,
            "業績悪化": -3,
            "赤字": -3,

            "減配": -4,
            "下落": -4,
            "特別損失": -4,
            "営業赤字": -4,

            "粉飾決算": -5,
        }

    # =========================
    # 重複除去
    # =========================
    def _deduplicate(self, texts):

        seen = set()

        result = []

        for text in texts:

            key = text[:100]

            if key in seen:
                continue

            seen.add(key)

            result.append(text)

        return result

    # =========================
    # 材料スコア
    # =========================
    def _material_score(self, text):

        score = 0

        text = str(text)

        for keyword, value in self.keywords.items():

            if keyword in text:

                score += value

        return score

    # =========================
    # ソース重み
    # =========================
    def _source_weight(self):

        return 1.0

    # =========================
    # センチメント取得
    # =========================
    def get_sentiment(
        self,
        code,
        name
    ):

        try:

            news_items = (
                self.collector.fetch_all(
                    code,
                    name
                )
            )

            news_items = (
                self._deduplicate(
                    news_items
                )
            )

            filtered = (
                self.filter.filter_texts(
                    news_items,
                    name
                )
            )

            total_score = 0

            for text in filtered:

                score = (
                    self._material_score(
                        text
                    )
                )

                total_score += (
                    score
                    *
                    self._source_weight()
                )

            print(
                
                f"{code} {name} "
                
            )

            sentiment = max(
                min(
                    total_score / 30.0,
                    1.0
                ),
                -1.0
            )

            return round(
                sentiment,
                4
            )

        except Exception as e:

            print(
                "[Sentiment Error]",
                e
            )

            return 0.0