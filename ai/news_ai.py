from core.news.sentiment_engine import SentimentEngine
from core.news.theme_detector import ThemeDetector
from core.news.stock_context import StockContext


class NewsAI:

    def __init__(self):

        self.sentiment_engine = SentimentEngine()

        self.theme_detector = ThemeDetector()

        self.stock_context = StockContext()

    def run(self, code, name):

        try:

            sentiment = self.sentiment_engine.get_sentiment(
                code,
                name
            )

            theme_score, themes = self.theme_detector.analyze(
                name
            )

            context_score = self.stock_context.get_context_score(
                name
            )

            # =========================
            # 合成
            # =========================
            final_score = (
                (sentiment * 40) +
                (theme_score * 0.5) +
                (context_score * 20)
            )

            final_score = max(
                min(final_score, 100),
                0
            )

            return {
                "news_score": round(final_score, 2),
                "sentiment": round(sentiment, 2),
                "theme_score": round(theme_score, 2),
                "themes": themes,
                "context_score": round(context_score, 2)
            }

        except Exception as e:

            print("NEWS AI ERROR:", e)

            return {
                "news_score": 50,
                "sentiment": 0,
                "theme_score": 0,
                "themes": [],
                "context_score": 0
            }