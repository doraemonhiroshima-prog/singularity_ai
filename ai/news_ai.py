# ai/news_ai.py

from core.news.sentiment_engine import (
    SentimentEngine
)

from core.news.theme_detector import (
    ThemeDetector
)

from core.news.stock_context import (
    StockContext
)


class NewsAI:

    def __init__(self):

        self.sentiment_engine = (
            SentimentEngine()
        )

        self.theme_detector = (
            ThemeDetector()
        )

        self.stock_context = (
            StockContext()
        )

    def run(
        self,
        code,
        name,
        df=None
    ):

        try:

            sentiment = (
                self.sentiment_engine
                .get_sentiment(
                    code,
                    name
                )
            )

            news_text = ""

            try:

                collector = (
                    self.sentiment_engine
                    .collector
                )

                news_text = (
                    collector.fetch_all(
                        code,
                        name
                    )
                )

            except:
                pass

            theme_score, themes = (
                self.theme_detector.analyze(
                    news_text
                )
            )

            context_score = (
                self.stock_context
                .get_context_score(
                    name,
                    themes
                )
            )

            score = (

                (sentiment + 1)
                * 50

                +

                theme_score * 0.20

                +

                context_score * 20

            )

            score = max(
                min(score, 100),
                0
            )
            
            return {

                "score":
                    round(score, 2),

                "sentiment":
                    round(sentiment, 3),

                "theme_score":
                    round(theme_score, 2),

                "themes":
                    themes,

                "context_score":
                    round(context_score, 2)
            }

        except Exception as e:

            print(
                "NEWS AI ERROR:",
            
                e
            )

            return {
                "score": 50
            }