import requests
from datetime import datetime, timedelta


class NewsAI:

    def __init__(self):

        self.api_key = "ここにAPIキー"

        # =========================
        # 銘柄名マップ（重要）
        # =========================
        self.company_map = {
            "7203.T": "トヨタ",
            "6758.T": "ソニー",
            "9984.T": "ソフトバンク",
            # 必要に応じて追加
        }

    # =========================
    # 銘柄名取得
    # =========================
    def get_query(self, code):

        if code in self.company_map:
            return self.company_map[code]

        return code.replace(".T", "")

    # =========================
    # 感情分析
    # =========================
    def sentiment_score(self, text):

        pos_words = [
            "上方修正","増益","最高益","好調","成長","拡大","受注",
            "提携","黒字","回復","増配","買収","新製品"
        ]

        neg_words = [
            "下方修正","減益","赤字","不振","悪化","縮小",
            "不祥事","下落","損失","リストラ","破産"
        ]

        score = 0

        for w in pos_words:
            if w in text:
                score += 20

        for w in neg_words:
            if w in text:
                score -= 20

        return score

    # =========================
    # インパクト
    # =========================
    def impact_score(self, text):

        strong = ["過去最高","大幅","急騰","ストップ高"]
        weak = ["やや","小幅"]

        score = 0

        for w in strong:
            if w in text:
                score += 30

        for w in weak:
            if w in text:
                score -= 10

        return score

    # =========================
    # 関連度
    # =========================
    def relevance_score(self, text, keyword):

        if keyword in text:
            return 30

        return 10

    # =========================
    # メイン
    # =========================
    def analyze(self, code):

        try:
            keyword = self.get_query(code)

            # =========================
            # 時間制限（超重要）
            # =========================
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

            url = (
                f"https://newsapi.org/v2/everything?"
                f"q={keyword}&language=jp&from={yesterday}&sortBy=publishedAt&apiKey={self.api_key}"
            )

            res = requests.get(url).json()
            articles = res.get("articles", [])[:10]

            if not articles:
                return 0

            total_score = 0

            for a in articles:

                title = a.get("title", "")
                desc = a.get("description", "")

                text = f"{title} {desc}"

                s = 0

                s += self.sentiment_score(text)
                s += self.impact_score(text)
                s += self.relevance_score(text, keyword)

                total_score += s

            # 平均
            score = total_score / len(articles)

            # 正規化
            score = max(min(score, 100), -100)

            return score

        except Exception as e:
            print("NEWS ERROR:", e)
            return 0
