from .news_collector import NewsCollector
import re
import time


class SentimentEngine:

    def __init__(self):
        self.collector = NewsCollector()

    # =========================
    # 重複削除
    # =========================
    def _deduplicate(self, texts):

        seen = set()
        unique = []

        for t in texts:
            key = t[:100]
            if key not in seen:
                seen.add(key)
                unique.append(t)

        return unique

    # =========================
    # 材料強度
    # =========================
    def _material_score(self, text):

        score = 0

        # 超強
        if "上方修正" in text:
            score += 3
        if "決算" in text:
            score += 3
        if "最高益" in text:
            score += 3

        # 中
        if "提携" in text:
            score += 2
        if "新製品" in text:
            score += 2

        # 弱
        if "期待" in text:
            score += 1

        # 悪材料
        if "下方修正" in text:
            score -= 3
        if "赤字" in text:
            score -= 3
        if "不正" in text:
            score -= 4

        return score

    # =========================
    # 時間重み（仮）
    # =========================
    def _time_weight(self, text):

        # RSSは時間取れないので簡易
        # 将来ここ強化
        return 1.0

    # =========================
    # ソース重み
    # =========================
    def _source_weight(self, source):

        weights = {
            "tdnet": 2.5,
            "kabutan": 1.8,
            "yahoo": 1.5,
            "google": 1.2,
            "minkabu": 1.0
        }

        return weights.get(source, 1.0)

    # =========================
    # メイン
    # =========================
    def get_sentiment(self, code, name):

        texts = []

        sources = {
            "google": self.collector.google(name),
            "yahoo": self.collector.yahoo(code),
            "kabutan": self.collector.kabutan(code),
            "minkabu": self.collector.minkabu(code),
            "tdnet": self.collector.tdnet()
        }

        # =========================
        # 分割
        # =========================
        for src, text in sources.items():
            parts = re.split("[\n\r]", text)
            for p in parts:
                if len(p) > 20:
                    texts.append((src, p))

        # =========================
        # 重複削除
        # =========================
        texts = self._deduplicate([t[1] for t in texts])

        # =========================
        # スコア計算
        # =========================
        score = 0

        for t in texts:

            material = self._material_score(t)
            time_w = self._time_weight(t)

            score += material * time_w

        # 正規化
        return max(min(score / 20, 1), -1)