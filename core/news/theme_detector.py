import random


class ThemeDetector:

    def __init__(self):

        self.themes = {
            "AI": ["AI", "人工知能", "半導体", "データセンター"],
            "EV": ["EV", "電気自動車", "電池", "リチウム"],
            "防衛": ["防衛", "ミサイル", "軍需"],
            "半導体": ["半導体", "チップ", "TSMC"],
            "バイオ": ["バイオ", "創薬", "医薬"],
            "宇宙": ["宇宙", "ロケット"],
            "DX": ["DX", "クラウド", "SaaS"],
        }

    # =========================
    # テーマ解析（強化版）
    # =========================
    def analyze(self, name):

        score = 0
        matched = []

        for theme, words in self.themes.items():

            hit_count = 0

            for w in words:
                if w in name:
                    hit_count += 1

            if hit_count > 0:
                # ヒット数で強さ変化
                s = min(hit_count * 15, 40)

                score += s
                matched.append((theme, s))

        # =========================
        # ノーヒット対策（探索）
        # =========================
        if score == 0:
            score += random.randint(5, 15)

        # =========================
        # 上限制御
        # =========================
        score = min(score, 100)

        return score, matched